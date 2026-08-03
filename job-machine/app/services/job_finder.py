from __future__ import annotations

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
from sqlalchemy.orm import Session

from app.config import ROOT, get_settings
from app.models import Application, Job
from app.services.active_check import verify_jobs_active
from app.services.agent_log import log_action
from app.services.filters import (
    format_estimated_salary,
    is_priority_remote_company,
    level_hint,
    match_reason,
    normalize,
    should_keep,
    verify_remote,
)
from app.services.portfolio_matcher import match_portfolio
from app.services.production import (
    careers_url_for_job,
    is_placeholder_company,
    is_production_eligible,
    source_display,
)
from app.services.scorer import score_job
from app.services.sources import (
    fetch_arbeitnow,
    fetch_ashby_board,
    fetch_greenhouse_board,
    fetch_jobicy,
    fetch_lever_company,
    fetch_remoteok,
    fetch_remotive,
    fetch_with_retry,
    fetch_workable_company,
)
from app.services.source_policy import (
    is_allowed_free_source,
    is_paid_board_job,
    is_staffing_agency_without_employer,
    source_policy_summary,
)


def _write_last_refresh(payload: dict[str, Any]) -> None:
    path = ROOT / "data" / "last_refresh.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def read_last_refresh() -> dict[str, Any] | None:
    path = ROOT / "data" / "last_refresh.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


async def search_jobs(
    *,
    strict_level: bool = True,
    fully_remote_only: bool = True,
    us_only: bool = True,
    min_salary: float = 60000,
    prefer_no_degree: bool = True,
    block_five_plus_years: bool = True,
    quick_filters: list[str] | None = None,
    require_salary_listed: bool = False,
    verify_active: bool = True,
) -> dict[str, Any]:
    """PRODUCTION MODE: live sources only, verified remote, active postings, transparent Match Score."""
    settings = get_settings()
    collected: list[dict[str, Any]] = []
    errors: list[str] = []
    rejected_placeholder = 0
    rejected_unverified = 0
    rejected_inactive = 0
    rejected_paid_board = 0
    rejected_staffing = 0

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        # Concurrent free-source fetches only (paid boards never registered)
        tasks: list[tuple[str, Any]] = [
            ("remoteok", lambda: fetch_remoteok(client)),
            ("remotive", lambda: fetch_remotive(client)),
            ("jobicy", lambda: fetch_jobicy(client)),
            ("arbeitnow", lambda: fetch_arbeitnow(client)),
        ]
        for board in settings.greenhouse_board_list:
            b = board
            tasks.append((f"greenhouse:{b}", lambda b=b: fetch_greenhouse_board(client, b)))
        for company in settings.lever_company_list:
            c = company
            tasks.append((f"lever:{c}", lambda c=c: fetch_lever_company(client, c)))
        for board in settings.ashby_board_list:
            b = board
            tasks.append((f"ashby:{b}", lambda b=b: fetch_ashby_board(client, b)))
        for company in settings.workable_company_list:
            c = company
            tasks.append((f"workable:{c}", lambda c=c: fetch_workable_company(client, c)))

        async def _one(name: str, factory):
            try:
                rows = await fetch_with_retry(factory, attempts=2, label=name)
                return name, rows, None
            except Exception as exc:  # noqa: BLE001
                return name, [], str(exc)

        results = await asyncio.gather(*[_one(n, f) for n, f in tasks])
        for name, rows, err in results:
            if err:
                errors.append(f"{name}: {err}")
                log_action("source_failed", source=name, error=err)
            else:
                collected.extend(rows)
                log_action("source_ok", source=name, count=len(rows))

    candidates: list[dict[str, Any]] = []
    for job in collected:
        paid, paid_reason = is_paid_board_job(job)
        if paid:
            rejected_paid_board += 1
            log_action("rejected_paid_board", source=job.get("source"), reason=paid_reason, url=job.get("url"))
            continue

        allowed, allow_reason = is_allowed_free_source(job)
        if not allowed:
            rejected_paid_board += 1
            log_action("rejected_disallowed_source", source=job.get("source"), reason=allow_reason)
            continue

        if is_staffing_agency_without_employer(job):
            rejected_staffing += 1
            continue

        ok, reason = is_production_eligible(job)
        if not ok:
            rejected_placeholder += 1
            continue

        verification = verify_remote(job)
        job["remote_verification"] = verification
        job["remote_verified"] = verification["verified"]
        job["remote_verified_label"] = verification["label"]
        job["is_remote"] = verification["verified"]
        job["careers_url"] = careers_url_for_job(job)
        job["source_display"] = source_display(str(job.get("source") or ""))

        if fully_remote_only and not verification["verified"]:
            rejected_unverified += 1
            continue

        if not should_keep(
            job,
            strict_level=strict_level,
            fully_remote_only=fully_remote_only,
            us_only=us_only,
            min_salary=min_salary,
            prefer_no_degree=prefer_no_degree,
            block_five_plus_years=block_five_plus_years,
            quick_filters=quick_filters,
            require_salary_listed=require_salary_listed,
        ):
            continue
        candidates.append(job)

    if verify_active and candidates:
        before = len(candidates)
        candidates = await verify_jobs_active(candidates)
        rejected_inactive = before - len(candidates)

    kept: list[dict[str, Any]] = []
    for job in candidates:
        job["level_hint"] = level_hint(job)
        score, breakdown = score_job(job)
        projects = match_portfolio(job)
        why = match_reason(job, projects)
        est_salary = format_estimated_salary(job)
        breakdown["why_match"] = why
        breakdown["estimated_salary"] = est_salary
        breakdown["portfolio_to_cite"] = [p.get("name") for p in projects[:4]]
        breakdown["remote_verification"] = job.get("remote_verification")
        breakdown["remote_verified"] = True
        breakdown["remote_verified_label"] = job.get("remote_verified_label")
        breakdown["careers_url"] = job.get("careers_url")
        breakdown["source_display"] = job.get("source_display")
        breakdown["active_check"] = job.get("active_check")
        job["score"] = score
        job["score_breakdown"] = breakdown
        job["matched_projects"] = projects
        job["match_reason"] = why
        job["match_percentage"] = score
        job["match_score"] = score
        job["interview_probability"] = None  # never invent
        job["estimated_salary"] = est_salary
        job["priority_remote_company"] = is_priority_remote_company(job)
        job["posting_url"] = job.get("url")
        job["date_found"] = datetime.utcnow().isoformat() + "Z"
        kept.append(job)

    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for job in kept:
        key = f"{normalize(job.get('company',''))}|{normalize(job.get('title',''))}"
        if key in seen:
            continue
        seen.add(key)
        deduped.append(job)
    kept = deduped

    kept.sort(
        key=lambda j: (
            float(j.get("match_score") or j.get("score") or 0),
            1 if j.get("priority_remote_company") else 0,
            1 if j.get("salary_text") or j.get("salary_min") else 0,
        ),
        reverse=True,
    )

    result = {
        "fetched": len(collected),
        "matched": len(kept),
        "rejected_placeholder": rejected_placeholder,
        "rejected_unverified_remote": rejected_unverified,
        "rejected_inactive": rejected_inactive,
        "rejected_paid_board": rejected_paid_board,
        "rejected_staffing_agency": rejected_staffing,
        "errors": errors,
        "jobs": kept,
        "ranking_mode": "transparent_match_score_v2",
        "remote_mode": "strict",
        "production_mode": True,
        "concurrent_sources": True,
        "free_sources_only": True,
        "refreshed_at": datetime.utcnow().isoformat() + "Z",
        "weights": {
            "skill_match": 0.35,
            "interview_readiness": 0.25,
            "remote_eligibility": 0.15,
            "salary_fit": 0.10,
            "career_growth": 0.05,
            "resume_match": 0.05,
            "portfolio_match": 0.05,
        },
        "filters_applied": {
            "min_salary": min_salary,
            "fully_remote_only": fully_remote_only,
            "us_remote": us_only,
            "verified_remote_only": True,
            "verify_active": verify_active,
            "entry_junior_associate": strict_level,
            "prefer_no_degree": prefer_no_degree,
            "block_five_plus_years": block_five_plus_years,
            "quick_filters": quick_filters or [],
            "require_salary_listed": require_salary_listed,
            "no_placeholders": True,
            "no_paid_job_boards": True,
            "no_staffing_without_employer": True,
        },
        "source_policy": source_policy_summary(),
        "sources_note": (
            "FREE SOURCES ONLY — Greenhouse, Lever, Ashby, Workable + free aggregators "
            "(RemoteOK, Remotive, Jobicy). Direct company careers OK. "
            "LinkedIn Easy Apply / Indeed / ZipRecruiter / Google Jobs / Built In / Wellfound / Otta "
            "allowed when free (manual import). "
            "PERMANENTLY EXCLUDED: We Work Remotely, FlexJobs, Remote Rocketship, and any pay-to-apply board. "
            "100% remote · US only · no staffing agencies without named employer · Auto-apply: OFF."
        ),
        "auto_apply": False,
    }
    _write_last_refresh(
        {
            "refreshed_at": result["refreshed_at"],
            "fetched": result["fetched"],
            "matched": result["matched"],
            "rejected_inactive": rejected_inactive,
            "rejected_placeholder": rejected_placeholder,
            "mode": "production",
        }
    )
    return result


def upsert_jobs(db: Session, jobs: list[dict[str, Any]]) -> int:
    added = 0
    for job in jobs:
        if is_placeholder_company(str(job.get("company") or "")):
            continue
        existing = (
            db.query(Job)
            .filter(Job.source == job["source"], Job.external_id == job["external_id"])
            .one_or_none()
        )
        tags = job.get("tags") or []
        tag_str = ", ".join(tags) if isinstance(tags, list) else str(tags)
        breakdown = job.get("score_breakdown") or {}
        if isinstance(breakdown, dict):
            breakdown = {
                **breakdown,
                "careers_url": job.get("careers_url") or breakdown.get("careers_url"),
                "source_display": job.get("source_display") or breakdown.get("source_display"),
                "active_check": job.get("active_check") or breakdown.get("active_check"),
            }
        payload = {
            "company": job["company"],
            "title": job["title"],
            "location": job.get("location") or "Remote",
            "is_remote": 1 if job.get("is_remote") or job.get("remote_verified") else 0,
            "salary_text": job.get("salary_text") or job.get("estimated_salary") or "",
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "url": job.get("url") or "",
            "description": job.get("description") or "",
            "tags": tag_str,
            "level_hint": job.get("level_hint") or "",
            "score": float(job.get("score") or 0),
            "score_breakdown": json.dumps(breakdown),
            "matched_projects": json.dumps(job.get("matched_projects") or []),
            "posted_at": job.get("posted_at"),
            "status": "new",
        }
        if existing:
            for k, v in payload.items():
                setattr(existing, k, v)
        else:
            db.add(
                Job(
                    external_id=job["external_id"],
                    source=job["source"],
                    found_at=datetime.utcnow(),
                    **payload,
                )
            )
            added += 1
    db.commit()
    return added


def purge_unverified_remote(db: Session) -> int:
    """Mark jobs that fail STRICT REMOTE verification so they leave the active feed."""
    removed = 0
    for row in db.query(Job).all():
        job = {
            "title": row.title,
            "company": row.company,
            "location": row.location,
            "description": row.description or "",
            "tags": row.tags or "",
            "source": row.source,
            "url": row.url,
            "is_remote": bool(row.is_remote),
        }
        if is_placeholder_company(row.company) or not is_production_eligible(job)[0]:
            row.status = "hidden-placeholder"
            removed += 1
            continue
        verification = verify_remote(job)
        breakdown = {}
        try:
            breakdown = json.loads(row.score_breakdown or "{}")
        except json.JSONDecodeError:
            breakdown = {}
        breakdown["remote_verification"] = verification
        breakdown["remote_verified"] = verification["verified"]
        breakdown["remote_verified_label"] = verification["label"]
        breakdown["careers_url"] = careers_url_for_job({**job, "source": row.source, "url": row.url})
        breakdown["source_display"] = source_display(row.source)
        row.score_breakdown = json.dumps(breakdown)
        row.is_remote = 1 if verification["verified"] else 0
        if not verification["verified"]:
            if row.status not in {"hidden-unverified-remote", "hidden-placeholder", "hidden-inactive"}:
                row.status = "hidden-unverified-remote"
                removed += 1
        elif row.status in {"hidden-unverified-remote"}:
            row.status = "new"
    db.commit()
    return removed


def purge_placeholders(db: Session) -> dict[str, int]:
    """Remove demo/fake employers from jobs + applications + local packets."""
    import shutil

    jobs_removed = 0
    apps_removed = 0
    for row in db.query(Job).all():
        if is_placeholder_company(row.company):
            db.query(Application).filter(Application.job_id == row.id).delete()
            db.delete(row)
            jobs_removed += 1
    for row in db.query(Application).all():
        if is_placeholder_company(row.company):
            db.delete(row)
            apps_removed += 1
    db.commit()

    packets = ROOT / "data" / "interview_packets"
    packet_dirs = 0
    if packets.exists():
        for folder in list(packets.iterdir()):
            if not folder.is_dir():
                continue
            name = folder.name.lower()
            if any(x in name for x in ["acme", "example", "demo-company", "test-company", "sample"]):
                shutil.rmtree(folder, ignore_errors=True)
                packet_dirs += 1
    return {"jobs_removed": jobs_removed, "apps_removed": apps_removed, "packet_dirs_removed": packet_dirs}


def purge_paid_boards(db: Session) -> dict[str, int]:
    """Hide jobs from permanently blacklisted paid boards (WWR, FlexJobs, Remote Rocketship, etc.)."""
    hidden = 0
    apps_flagged = 0
    for row in db.query(Job).all():
        job = {
            "title": row.title,
            "company": row.company,
            "location": row.location,
            "description": row.description or "",
            "tags": row.tags or "",
            "source": row.source,
            "url": row.url,
        }
        paid, reason = is_paid_board_job(job)
        allowed, allow_reason = is_allowed_free_source(job)
        if paid or not allowed:
            if row.status != "hidden-paid-board":
                row.status = "hidden-paid-board"
                hidden += 1
            try:
                bd = json.loads(row.score_breakdown or "{}")
            except json.JSONDecodeError:
                bd = {}
            bd["paid_board_block"] = {
                "blocked": True,
                "reason": reason or allow_reason,
                "checked_at": datetime.utcnow().isoformat() + "Z",
            }
            row.score_breakdown = json.dumps(bd)
            for app in db.query(Application).filter(Application.job_id == row.id).all():
                if app.status not in {"applied", "offer", "accepted", "rejected", "withdrawn"}:
                    note = f"\n[{datetime.utcnow().isoformat()}Z] Hidden: paid/disallowed board ({reason or allow_reason})."
                    app.notes = ((app.notes or "").rstrip() + note).strip()
                    apps_flagged += 1
    db.commit()
    log_action("purge_paid_boards", jobs_hidden=hidden, apps_flagged=apps_flagged)
    return {"jobs_hidden": hidden, "apps_flagged": apps_flagged}


def mark_inactive_job(db: Session, job_id: int, reason: str = "inactive") -> None:
    row = db.get(Job, job_id)
    if not row:
        return
    row.status = "hidden-inactive"
    try:
        bd = json.loads(row.score_breakdown or "{}")
    except json.JSONDecodeError:
        bd = {}
    bd["active_check"] = {"active": False, "reason": reason, "checked_at": datetime.utcnow().isoformat() + "Z"}
    row.score_breakdown = json.dumps(bd)
    db.commit()
