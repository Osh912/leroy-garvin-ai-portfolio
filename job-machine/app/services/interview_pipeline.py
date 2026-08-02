from __future__ import annotations

import json
from datetime import date, datetime, time, timedelta
from typing import Any

from sqlalchemy.orm import Session

from app.models import Application, Job
from app.services.cover_letter import generate_cover_letter
from app.services.filters import (
    format_estimated_salary,
    match_reason,
    should_keep,
    verify_remote,
)
from app.services.interview_prep import build_interview_prep
from app.services.job_finder import purge_unverified_remote, search_jobs, upsert_jobs
from app.services.packet_store import save_packet_locally
from app.services.pipeline_stages import (
    interview_probability_from_job,
)
from app.services.portfolio_matcher import match_portfolio
from app.services.resume_tailor import tailor_resume
from app.services.scorer import score_job


def _job_dict(row: Job) -> dict[str, Any]:
    return {
        "title": row.title,
        "company": row.company,
        "location": row.location,
        "description": row.description or "",
        "tags": row.tags or "",
        "is_remote": bool(row.is_remote),
        "salary_min": row.salary_min,
        "salary_max": row.salary_max,
        "salary_text": row.salary_text or "",
        "source": row.source,
        "url": row.url,
        "score": row.score,
        "score_breakdown": row.score_breakdown,
    }


def rank_jobs_by_interview_probability(db: Session, *, limit: int = 10) -> list[Job]:
    """Return verified live jobs ranked by transparent Match Score (production)."""
    from app.services.production import is_placeholder_company, is_production_eligible

    candidates = (
        db.query(Job)
        .filter(~Job.status.in_(["hidden-unverified-remote", "hidden-placeholder", "hidden-inactive"]))
        .order_by(Job.score.desc())
        .limit(200)
        .all()
    )
    scored: list[tuple[float, Job]] = []
    for row in candidates:
        if is_placeholder_company(row.company):
            continue
        jd = _job_dict(row)
        jd["url"] = row.url
        if not is_production_eligible(jd)[0]:
            continue
        if not verify_remote(jd)["verified"]:
            continue
        if not should_keep(jd):
            continue
        try:
            bd = json.loads(row.score_breakdown or "{}")
        except json.JSONDecodeError:
            bd = {}
        if bd.get("scoring_mode") != "transparent_match_score_v1":
            score, breakdown = score_job(jd)
            projects = match_portfolio(jd)
            why = match_reason(jd, projects)
            breakdown["why_match"] = why
            row.score = score
            row.score_breakdown = json.dumps(breakdown)
            row.matched_projects = json.dumps(projects)
            match = score
        else:
            match = float(bd.get("match_score") or row.score or 0)
        scored.append((match, row))
    scored.sort(key=lambda t: t[0], reverse=True)
    db.commit()
    return [t[1] for t in scored[:limit]]


def prepare_top_packets(db: Session, *, limit: int = 10) -> list[dict[str, Any]]:
    """
    For Top N jobs by interview probability:
    generate resume, cover letter, portfolio match, why-fit, save locally.
    Status becomes 'ready' — NOT applied. Requires Leroy's approval.
    """
    top = rank_jobs_by_interview_probability(db, limit=limit)
    results: list[dict[str, Any]] = []

    for rank, row in enumerate(top, start=1):
        jd = _job_dict(row)
        score, breakdown = score_job(jd)
        projects = match_portfolio(jd)
        why = match_reason(jd, projects)
        est = format_estimated_salary(jd)
        match = float(breakdown.get("match_score") or score)

        resume, resume_ai, resume_warn = tailor_resume(jd, projects)
        cover, cover_ai, cover_warn = generate_cover_letter(jd, projects)

        breakdown["why_match"] = why
        breakdown["estimated_salary"] = est
        breakdown["portfolio_to_cite"] = [p.get("name") for p in projects[:4]]
        breakdown["match_score"] = match
        breakdown["match_percentage"] = match

        row.score = score
        row.score_breakdown = json.dumps(breakdown)
        row.matched_projects = json.dumps(projects)

        prep = build_interview_prep(jd, projects, why_match=why)
        paths = save_packet_locally(
            job_id=row.id,
            company=row.company,
            title=row.title,
            resume=resume,
            cover=cover,
            prep=prep,
            projects=projects,
            why_match=why,
            interview_probability=match,  # stored as match score, not invented IP
            match_percentage=match,
            estimated_salary=est,
            status="ready",
        )

        # Upsert application as ready (awaiting approval) — never applied
        existing = (
            db.query(Application)
            .filter(Application.job_id == row.id)
            .order_by(Application.updated_at.desc())
            .first()
        )
        notes = (
            f"[Interview Pipeline rank #{rank}] Match Score {match}% · {why}\n"
            f"Packet saved locally. Awaiting Leroy approval to apply. Auto-apply: OFF."
        )
        if existing:
            # Don't overwrite applied+ progress stages
            if existing.status in {"saved", "ready", ""}:
                existing.status = "ready"
            existing.tailored_resume = resume
            existing.cover_letter = cover
            existing.interview_prep = json.dumps(prep)
            existing.portfolio_refs = json.dumps(projects)
            existing.application_score = score
            existing.salary = est if est != "Not listed" else (existing.salary or row.salary_text)
            existing.notes = notes
            existing.updated_at = datetime.utcnow()
            app_row = existing
        else:
            app_row = Application(
                job_id=row.id,
                company=row.company,
                position=row.title,
                salary=est if est != "Not listed" else (row.salary_text or ""),
                location=row.location,
                date_applied=None,
                status="ready",
                notes=notes,
                tailored_resume=resume,
                cover_letter=cover,
                interview_prep=json.dumps(prep),
                portfolio_refs=json.dumps(projects),
                application_score=score,
            )
            db.add(app_row)

        if row.status in {"new", "saved", "ready", "hidden-unverified-remote"}:
            row.status = "ready"

        db.commit()
        db.refresh(app_row)

        results.append(
            {
                "rank": rank,
                "job_id": row.id,
                "application_id": app_row.id,
                "company": row.company,
                "title": row.title,
                "location": row.location,
                "url": row.url,
                "match_score": match,
                "match_percentage": match,
                "estimated_salary": est,
                "why_match": why,
                "projects": projects[:4],
                "package_ready": True,
                "status": app_row.status,
                "approval_required": True,
                "auto_apply": False,
                "packet_paths": paths,
                "used_ai": resume_ai or cover_ai or bool(prep.get("used_ai")),
                "truth_warnings": list(dict.fromkeys(resume_warn + cover_warn + (prep.get("truth_warnings") or []))),
            }
        )
    return results


async def morning_refresh(db: Session, *, prepare_packets: bool = True) -> dict[str, Any]:
    """
    Morning Interview Pipeline refresh:
    1) Fetch verified remote jobs
    2) Rank by interview probability
    3) Prepare Top 10 packets (no auto-apply)
    """
    result = await search_jobs(
        strict_level=True,
        fully_remote_only=True,
        us_only=True,
        min_salary=60000,
        prefer_no_degree=True,
        block_five_plus_years=True,
    )
    purged = purge_unverified_remote(db)
    added = upsert_jobs(db, result["jobs"])
    packets: list[dict[str, Any]] = []
    if prepare_packets:
        packets = prepare_top_packets(db, limit=10)

    # Persist morning run log locally
    log_dir = __import__("pathlib").Path(__file__).resolve().parents[2] / "data"
    log_dir.mkdir(parents=True, exist_ok=True)
    log = {
        "ran_at": datetime.utcnow().isoformat() + "Z",
        "fetched": result["fetched"],
        "matched": result["matched"],
        "added": added,
        "purged_unverified_remote": purged,
        "rejected_unverified_remote": result.get("rejected_unverified_remote", 0),
        "packets_prepared": len(packets),
        "auto_apply": False,
        "top_10": packets,
    }
    (log_dir / "morning_refresh_last.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
    return log


def approve_application(db: Session, app_id: int) -> Application:
    """Leroy explicitly approves applying — the only path to 'applied'."""
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    if row.status == "rejected":
        raise ValueError("Cannot approve a rejected application")
    row.status = "applied"
    row.date_applied = date.today()
    if not row.follow_up_date:
        row.follow_up_date = date.today() + timedelta(days=5)
    row.notes = (row.notes or "") + f"\n[{datetime.utcnow().isoformat()}Z] Approved by Leroy — marked Applied. Auto-apply never used."
    row.updated_at = datetime.utcnow()
    job = db.get(Job, row.job_id) if row.job_id else None
    if job:
        job.status = "applied"
    db.commit()
    db.refresh(row)
    return row


def highest_probability_this_week(db: Session) -> dict[str, Any] | None:
    today = date.today()
    week_end = today + timedelta(days=7)
    apps = db.query(Application).all()
    best = None
    best_ip = -1.0
    for a in apps:
        if a.status in {"rejected", "offer"}:
            continue
        # Prefer apps with interview this week, else ready/saved high IP
        ip = float(a.application_score or 0)
        job = db.get(Job, a.job_id) if a.job_id else None
        if job:
            ip = max(ip, interview_probability_from_job(job))
        in_window = False
        if a.interview_date and today <= a.interview_date <= week_end:
            in_window = True
        if a.status in {"ready", "applied", "recruiter_contact", "first_interview", "technical_interview", "final_interview"}:
            in_window = True
        if not in_window:
            continue
        if ip > best_ip:
            best_ip = ip
            best = {
                "application_id": a.id,
                "job_id": a.job_id,
                "company": a.company,
                "position": a.position,
                "status": a.status,
                "interview_date": a.interview_date.isoformat() if a.interview_date else None,
                "interview_probability": best_ip,
            }
    return best
