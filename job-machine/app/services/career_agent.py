from __future__ import annotations

"""
AI Career Agent — morning orchestration + Daily Brief.
Calls existing morning_refresh / scoring / packets. Never auto-submits or emails.
"""

import json
import re
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.config import ROOT
from app.models import Application, Job, RecruiterContact
from app.services.filters import load_profile, normalize
from app.services.pipeline_stages import normalize_status

BRIEFS_DIR = ROOT / "data" / "daily_briefs"
AGENT_LAST = ROOT / "data" / "career_agent_last.json"
HIGH_SCORE_THRESHOLD = 80.0
ALERT_SCORE_THRESHOLD = 90.0

# Technologies frequently seen in remote ops/automation postings (for gap analysis only)
TECH_VOCAB = [
    "python",
    "sql",
    "javascript",
    "typescript",
    "n8n",
    "airtable",
    "zapier",
    "make.com",
    "salesforce",
    "zendesk",
    "jira",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "langchain",
    "openai",
    "anthropic",
    "chatgpt",
    "claude",
    "rag",
    "api",
    "rest",
    "graphql",
    "looker",
    "tableau",
    "snowflake",
    "dbt",
    "hubspot",
    "notion",
    "slack",
    "twilio",
]


def _parse_meta(row: Application) -> dict[str, Any]:
    try:
        data = json.loads(getattr(row, "analytics_json", None) or "{}")
    except json.JSONDecodeError:
        data = {}
    return data if isinstance(data, dict) else {}


def _profile_skill_set() -> set[str]:
    p = load_profile()
    skills = [normalize(s) for s in (p.get("skills") or [])]
    tools = [normalize(t) for t in (p.get("tools") or [])]
    return set(skills + tools)


async def run_career_agent_morning(
    db: Session,
    *,
    prepare_packets: bool = True,
    force: bool = False,
    trigger: str = "scheduler",
) -> dict[str, Any]:
    """
    Autonomous / manual RUN NOW:
    search boards → verify active → purge → score → packets → prep → analytics brief.
    Never auto-submits. Never sends email.
    """
    from app.services.agent_log import acquire_run_lock, log_action, release_run_lock
    from app.services.company_cache import set_cached_company
    from app.services.interview_pipeline import morning_refresh
    from app.services.recruiter_analytics import build_analytics_dashboard

    if not acquire_run_lock(force=force):
        log_action("run_skipped_duplicate", trigger=trigger)
        return {
            "ok": False,
            "skipped": True,
            "reason": "Another agent run is already in progress. Use RUN NOW with force, or wait.",
            "auto_apply": False,
            "auto_email": False,
        }

    try:
        log_action("career_agent_start", trigger=trigger, force=force)
        refresh_log = await morning_refresh(db, prepare_packets=prepare_packets)
        # Cache lightweight company signals from top packets (local only)
        for p in (refresh_log.get("top_10") or [])[:10]:
            set_cached_company(
                p.get("company") or "",
                {
                    "title": p.get("title"),
                    "match_score": p.get("match_score") or p.get("match_percentage"),
                    "why_match": p.get("why_match"),
                    "cached_from": "career_agent_run",
                },
            )
        # Refresh analytics snapshot (local compute — no side-effect to APIs)
        try:
            analytics = build_analytics_dashboard(db)
        except Exception as exc:  # noqa: BLE001
            analytics = {"error": str(exc)}
            log_action("analytics_update_failed", error=str(exc))

        brief = build_daily_brief(db, refresh_log=refresh_log)
        brief["todays_brief"] = build_todays_brief(db, refresh_log=refresh_log, analytics=analytics)
        brief["notifications"] = _merge_notifications(brief.get("notifications") or [], db, refresh_log)
        save_daily_brief(brief)
        AGENT_LAST.parent.mkdir(parents=True, exist_ok=True)
        AGENT_LAST.write_text(
            json.dumps(
                {
                    "ran_at": brief["generated_at"],
                    "brief_date": brief["date"],
                    "trigger": trigger,
                    "mode": "ai_career_agent_2_0",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        log_action(
            "career_agent_complete",
            trigger=trigger,
            fetched=refresh_log.get("fetched"),
            matched=refresh_log.get("matched"),
            packets=refresh_log.get("packets_prepared"),
        )
        release_run_lock(ok=True, trigger=trigger)
        return {
            "ok": True,
            "mode": "ai_career_agent_2_0",
            "trigger": trigger,
            "auto_apply": False,
            "auto_email": False,
            "approval_required": True,
            "refresh": refresh_log,
            "brief": brief,
            "todays_brief": brief["todays_brief"],
            "notifications": brief.get("notifications") or [],
        }
    except Exception as exc:  # noqa: BLE001
        log_action("career_agent_failed", trigger=trigger, error=str(exc))
        release_run_lock(ok=False, error=str(exc))
        raise


async def run_now(db: Session, *, prepare_packets: bool = True) -> dict[str, Any]:
    """Manual RUN NOW — same pipeline as morning, force lock override."""
    return await run_career_agent_morning(db, prepare_packets=prepare_packets, force=True, trigger="run_now")


def build_daily_brief(db: Session, *, refresh_log: dict[str, Any] | None = None) -> dict[str, Any]:
    today = date.today()
    since = datetime.combine(today, datetime.min.time())
    jobs = db.query(Job).all()
    apps = db.query(Application).order_by(Application.updated_at.desc()).all()
    contacts = db.query(RecruiterContact).all()

    new_jobs = [j for j in jobs if j.found_at and j.found_at >= since and j.status not in {"inactive", "purged"}]
    # Prefer refresh log top_10 for best opportunities
    top_packets = (refresh_log or {}).get("top_10") or []
    scored = sorted(
        [j for j in jobs if j.status not in {"inactive", "purged"}],
        key=lambda j: float(j.score or 0),
        reverse=True,
    )
    best = [
        {
            "job_id": j.id,
            "company": j.company,
            "title": j.title,
            "score": round(float(j.score or 0), 1),
            "salary": j.salary_text or "Not listed",
            "url": j.url,
            "notify": float(j.score or 0) >= HIGH_SCORE_THRESHOLD,
        }
        for j in scored[:15]
    ]
    high_score = [b for b in best if b["notify"]]
    alert_90 = [b for b in best if float(b.get("score") or 0) >= ALERT_SCORE_THRESHOLD]
    # Highest interview probability = highest match score among tracked apps / jobs (transparent match, not invented %)
    highest = None
    if apps:
        top_app = max(apps, key=lambda a: float(a.application_score or 0))
        highest = {
            "application_id": top_app.id,
            "company": top_app.company,
            "position": top_app.position,
            "match_score": round(float(top_app.application_score or 0), 1),
            "status": normalize_status(top_app.status),
            "note": "Match Score from transparent ranking engine — not an invented interview %.",
        }
    elif best:
        highest = {
            "job_id": best[0]["job_id"],
            "company": best[0]["company"],
            "position": best[0]["title"],
            "match_score": best[0]["score"],
            "status": "new",
            "note": "Match Score from transparent ranking engine — not an invented interview %.",
        }

    company_counts = Counter(j.company for j in jobs if j.status not in {"inactive", "purged"})
    companies_hiring_repeatedly = [
        {"company": c, "open_roles_tracked": n} for c, n in company_counts.most_common(10) if n >= 2
    ]

    salary_trends = _salary_trends(jobs)
    missing_skills, freq_tech = _skill_gaps(jobs)
    cert_recs = _cert_recommendations(missing_skills)

    recruiters_viewing = [
        {
            "application_id": a.id,
            "company": a.company,
            "position": a.position,
            "recruiter_name": a.recruiter_name or "",
            "status": normalize_status(a.status),
        }
        for a in apps
        if normalize_status(a.status) == "recruiter_viewed"
    ]

    follow_ups_due = []
    for a in apps:
        if a.follow_up_date and a.follow_up_date <= today and normalize_status(a.status) not in {
            "rejected",
            "withdrawn",
            "accepted",
        }:
            follow_ups_due.append(
                {
                    "application_id": a.id,
                    "company": a.company,
                    "position": a.position,
                    "follow_up_date": a.follow_up_date.isoformat(),
                    "approval_required": True,
                    "auto_send": False,
                }
            )
    for c in contacts:
        if c.follow_up_date and c.follow_up_date <= today:
            follow_ups_due.append(
                {
                    "recruiter_contact_id": c.id,
                    "company": c.company,
                    "recruiter_name": c.recruiter_name,
                    "follow_up_date": c.follow_up_date.isoformat(),
                    "approval_required": True,
                    "auto_send": False,
                }
            )

    upcoming_interviews = _upcoming_interviews(apps, today)
    closing_soon = _jobs_closing_within_48h(jobs, apps)

    notifications = []
    if alert_90:
        notifications.append(
            {
                "type": "new_90_plus_matches",
                "threshold": ALERT_SCORE_THRESHOLD,
                "count": len(alert_90),
                "jobs": alert_90,
                "message": f"{len(alert_90)} job(s) scored ≥ {ALERT_SCORE_THRESHOLD}% Match Score — priority review (never auto-applied).",
            }
        )
    if high_score:
        notifications.append(
            {
                "type": "high_match_jobs",
                "threshold": HIGH_SCORE_THRESHOLD,
                "count": len(high_score),
                "jobs": high_score,
                "message": f"{len(high_score)} job(s) scored ≥ {HIGH_SCORE_THRESHOLD}% — review packets (approval required to apply).",
            }
        )
    if follow_ups_due:
        notifications.append(
            {
                "type": "follow_ups_due",
                "count": len(follow_ups_due),
                "message": f"{len(follow_ups_due)} follow-up(s) due — drafts only; never auto-sent.",
            }
        )
    if upcoming_interviews:
        notifications.append(
            {
                "type": "upcoming_interviews",
                "count": len(upcoming_interviews),
                "message": f"{len(upcoming_interviews)} upcoming interview(s) — generate Interview Intelligence before each.",
            }
        )
    high_pay = [
        b
        for b in best
        if isinstance(b.get("salary"), str)
        and any(x in b["salary"] for x in ["100", "110", "120", "130", "140", "150"])
    ]
    if high_pay:
        notifications.append(
            {
                "type": "high_paying_remote",
                "count": len(high_pay),
                "jobs": high_pay[:5],
                "message": f"{len(high_pay)} high-listed-salary remote match(es) in top ranked set (from posting text only).",
            }
        )

    brief = {
        "date": today.isoformat(),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "mode": "daily_brief",
        "fabricated": False,
        "auto_apply": False,
        "auto_email": False,
        "approval_required": True,
        "notify_threshold": HIGH_SCORE_THRESHOLD,
        "refresh_summary": {
            "fetched": (refresh_log or {}).get("fetched"),
            "matched": (refresh_log or {}).get("matched"),
            "added": (refresh_log or {}).get("added"),
            "packets_prepared": (refresh_log or {}).get("packets_prepared"),
            "purged_unverified_remote": (refresh_log or {}).get("purged_unverified_remote"),
        },
        "new_jobs_found": [
            {
                "job_id": j.id,
                "company": j.company,
                "title": j.title,
                "score": round(float(j.score or 0), 1),
                "url": j.url,
            }
            for j in sorted(new_jobs, key=lambda x: float(x.score or 0), reverse=True)[:40]
        ],
        "best_opportunities": best[:10],
        "highest_interview_probability": highest,
        "companies_hiring_repeatedly": companies_hiring_repeatedly,
        "salary_trends": salary_trends,
        "missing_skills_appearing_frequently": missing_skills,
        "frequently_requested_technologies": freq_tech,
        "recommended_certifications": cert_recs,
        "recruiters_viewing_applications": recruiters_viewing,
        "follow_ups_due_today": follow_ups_due,
        "upcoming_interviews": upcoming_interviews,
        "jobs_closing_within_48_hours": closing_soon,
        "packets_ready": top_packets[:10],
        "notifications": notifications,
        "notes": [
            "Notify Leroy only for jobs ≥ 80% Match Score.",
            "Packets require approval before apply. Auto-submit is OFF.",
            "Certification recommendations are research suggestions — Leroy has no fabricated certs.",
            "Company closing dates appear only when tracked; otherwise list is empty.",
        ],
    }
    return brief


def build_todays_brief(
    db: Session,
    *,
    refresh_log: dict[str, Any] | None = None,
    analytics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Dashboard-oriented Today's Brief — additive to Daily Brief."""
    today = date.today()
    since = datetime.combine(today, datetime.min.time())
    jobs = db.query(Job).all()
    apps = db.query(Application).all()
    live = [j for j in jobs if j.status not in {"inactive", "purged"}]
    verified = [j for j in live if j.is_remote]
    new_today = [j for j in live if j.found_at and j.found_at >= since]
    top10 = sorted(live, key=lambda j: float(j.score or 0), reverse=True)[:10]
    ready = sum(1 for a in apps if normalize_status(a.status) in {"ready", "saved"})
    sent = sum(1 for a in apps if a.date_applied or normalize_status(a.status) in {
        "applied",
        "recruiter_viewed",
        "recruiter_replied",
        "phone_screen",
        "technical_interview",
        "hiring_manager",
        "final_interview",
        "offer",
        "accepted",
    })
    replies = sum(
        1
        for a in apps
        if normalize_status(a.status)
        in {
            "recruiter_replied",
            "phone_screen",
            "technical_interview",
            "hiring_manager",
            "final_interview",
            "offer",
            "accepted",
        }
    )
    interviews = sum(
        1
        for a in apps
        if a.interview_date
        or normalize_status(a.status)
        in {"phone_screen", "technical_interview", "hiring_manager", "final_interview"}
    )
    offers = sum(1 for a in apps if normalize_status(a.status) in {"offer", "accepted"})
    salary = _salary_trends(live)
    company_counts = Counter(j.company for j in live)
    missing, freq = _skill_gaps(live)
    kpis = (analytics or {}).get("kpis") or {}
    return {
        "date": today.isoformat(),
        "jobs_searched_today": (refresh_log or {}).get("fetched"),
        "verified_remote_jobs": len(verified),
        "new_jobs_today": len(new_today),
        "top_10_opportunities": [
            {
                "job_id": j.id,
                "company": j.company,
                "title": j.title,
                "score": round(float(j.score or 0), 1),
                "salary": j.salary_text or "Not listed",
                "url": j.url,
            }
            for j in top10
        ],
        "applications_ready": ready,
        "applications_sent": sent,
        "recruiter_replies": replies,
        "interviews_scheduled": interviews,
        "offers": offers,
        "average_salary": salary.get("average"),
        "salary_samples": salary.get("samples"),
        "top_companies_hiring": [
            {"company": c, "roles": n} for c, n in company_counts.most_common(8)
        ],
        "skill_trends": freq[:10],
        "missing_keywords": missing[:10],
        "analytics_kpis": {
            "response_rate": kpis.get("recruiter_response_rate"),
            "interview_rate": kpis.get("interview_rate"),
            "follow_ups_due": kpis.get("follow_ups_due"),
        },
        "auto_apply": False,
        "auto_email": False,
        "fabricated": False,
        "scoring_mode": "transparent_match_score_v2",
    }


def _merge_notifications(
    base: list[dict[str, Any]],
    db: Session,
    refresh_log: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    apps = db.query(Application).all()
    # Recruiter replies / interview invitations from status transitions
    replies = [
        a
        for a in apps
        if normalize_status(a.status) in {"recruiter_replied", "recruiter_viewed"}
        and a.updated_at
        and a.updated_at.date() == date.today()
    ]
    if replies:
        base.append(
            {
                "type": "recruiter_replies",
                "count": len(replies),
                "message": f"{len(replies)} recruiter view/reply update(s) today — review tracker (no auto-email).",
            }
        )
    invites = [
        a
        for a in apps
        if normalize_status(a.status)
        in {"phone_screen", "technical_interview", "hiring_manager", "final_interview"}
        and a.updated_at
        and a.updated_at.date() == date.today()
    ]
    if invites:
        base.append(
            {
                "type": "interview_invitations",
                "count": len(invites),
                "message": f"{len(invites)} interview-stage update(s) today — open Interview Intelligence.",
            }
        )
    closing = _jobs_closing_within_48h(db.query(Job).all(), apps)
    if closing:
        base.append(
            {
                "type": "jobs_closing_48h",
                "count": len(closing),
                "items": closing,
                "message": f"{len(closing)} tracked deadline(s) within 48 hours (only when date is known).",
            }
        )
    return base


def save_daily_brief(brief: dict[str, Any]) -> Path:
    BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    path = BRIEFS_DIR / f"{brief['date']}.json"
    path.write_text(json.dumps(brief, indent=2), encoding="utf-8")
    latest = BRIEFS_DIR / "latest.json"
    latest.write_text(json.dumps(brief, indent=2), encoding="utf-8")
    return path


def load_latest_brief() -> dict[str, Any] | None:
    path = BRIEFS_DIR / "latest.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _salary_trends(jobs: list[Job]) -> dict[str, Any]:
    mids: list[float] = []
    for j in jobs:
        if j.status in {"inactive", "purged"}:
            continue
        if j.salary_min and j.salary_max:
            mids.append((float(j.salary_min) + float(j.salary_max)) / 2)
        elif j.salary_min:
            mids.append(float(j.salary_min))
        elif j.salary_max:
            mids.append(float(j.salary_max))
    if not mids:
        return {
            "samples": 0,
            "average": None,
            "median": None,
            "min": None,
            "max": None,
            "note": "No listed salaries in tracked jobs — trends unavailable (not invented).",
        }
    mids.sort()
    n = len(mids)
    median = mids[n // 2] if n % 2 else (mids[n // 2 - 1] + mids[n // 2]) / 2
    return {
        "samples": n,
        "average": round(sum(mids) / n, 0),
        "median": round(median, 0),
        "min": round(mids[0], 0),
        "max": round(mids[-1], 0),
        "note": "Computed only from salaries listed on tracked postings.",
    }


def _skill_gaps(jobs: list[Job]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    owned = _profile_skill_set()
    owned_flat = " ".join(owned)
    counts: Counter = Counter()
    for j in jobs:
        if j.status in {"inactive", "purged"}:
            continue
        blob = normalize(f"{j.title} {j.tags} {j.description}")
        for tech in TECH_VOCAB:
            if re.search(rf"\b{re.escape(tech)}\b", blob):
                counts[tech] += 1
    freq = [{"technology": t, "job_mentions": n} for t, n in counts.most_common(15)]
    missing = []
    for t, n in counts.most_common(20):
        if t not in owned_flat and n >= 2:
            missing.append(
                {
                    "skill_or_tech": t,
                    "job_mentions": n,
                    "in_profile": False,
                    "note": "Appears in postings more than in Leroy’s verified skills/tools list.",
                }
            )
    return missing[:12], freq


def _cert_recommendations(missing_skills: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Research suggestions only — never claim Leroy holds these."""
    mapping = {
        "aws": "AWS Cloud Practitioner (research only — not held)",
        "azure": "Microsoft Azure Fundamentals (research only — not held)",
        "salesforce": "Salesforce Admin trailhead modules (research only — not held)",
        "python": "Practical Python projects over certs — portfolio evidence preferred",
        "sql": "SQL practice via portfolio workflows — no fabricated cert",
        "itil": "ITIL Foundation (research only — not held)",
    }
    out = []
    for m in missing_skills[:8]:
        tech = m["skill_or_tech"]
        if tech in mapping:
            out.append(
                {
                    "related_to": tech,
                    "suggestion": mapping[tech],
                    "held_by_leroy": False,
                    "fabricated": False,
                }
            )
    if not out:
        out.append(
            {
                "related_to": "general",
                "suggestion": "Prioritize portfolio demos (n8n, Airtable, AI ops) over unverified certificates.",
                "held_by_leroy": False,
                "fabricated": False,
            }
        )
    # Profile states education/certifications empty — reinforce truth
    out.append(
        {
            "related_to": "truth",
            "suggestion": "Profile lists zero certifications — do not claim any on applications.",
            "held_by_leroy": False,
            "fabricated": False,
        }
    )
    return out


def _upcoming_interviews(apps: list[Application], today: date) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for a in apps:
        if a.interview_date and a.interview_date >= today:
            out.append(
                {
                    "application_id": a.id,
                    "company": a.company,
                    "position": a.position,
                    "interview_date": a.interview_date.isoformat(),
                    "stage": normalize_status(a.status),
                }
            )
        meta = _parse_meta(a)
        for ev in meta.get("interview_calendar") or []:
            d = (ev.get("date") or "")[:10]
            try:
                ed = date.fromisoformat(d)
            except ValueError:
                continue
            if ed >= today:
                out.append(
                    {
                        "application_id": a.id,
                        "company": ev.get("company") or a.company,
                        "position": a.position,
                        "interview_date": ed.isoformat(),
                        "time": ev.get("time") or "",
                        "stage": ev.get("interview_stage") or normalize_status(a.status),
                        "meeting_link": ev.get("meeting_link") or "",
                    }
                )
    # dedupe
    seen = set()
    unique = []
    for item in sorted(out, key=lambda x: (x.get("interview_date") or "", x.get("time") or "")):
        key = (item.get("application_id"), item.get("interview_date"), item.get("time"))
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def _jobs_closing_within_48h(jobs: list[Job], apps: list[Application]) -> list[dict[str, Any]]:
    """Only include deadlines explicitly stored or parseable — never invent closing dates."""
    now = datetime.utcnow()
    horizon = now + timedelta(hours=48)
    out: list[dict[str, Any]] = []
    for a in apps:
        meta = _parse_meta(a)
        raw = meta.get("closing_date") or meta.get("application_deadline")
        if not raw:
            continue
        try:
            dt = datetime.fromisoformat(str(raw).replace("Z", ""))
        except ValueError:
            try:
                dt = datetime.combine(date.fromisoformat(str(raw)[:10]), datetime.min.time())
            except ValueError:
                continue
        if now <= dt <= horizon:
            out.append(
                {
                    "application_id": a.id,
                    "company": a.company,
                    "position": a.position,
                    "closes_at": dt.isoformat(),
                    "source": "application.analytics_json",
                }
            )
    for j in jobs:
        # Parse common deadline phrases only when an ISO-like date is present in description
        m = re.search(
            r"(?:apply by|closes? on|closing date|deadline)[:\s]+(\d{4}-\d{2}-\d{2})",
            j.description or "",
            re.I,
        )
        if not m:
            continue
        try:
            dt = datetime.combine(date.fromisoformat(m.group(1)), datetime.min.time())
        except ValueError:
            continue
        if now <= dt <= horizon:
            out.append(
                {
                    "job_id": j.id,
                    "company": j.company,
                    "title": j.title,
                    "closes_at": dt.isoformat(),
                    "source": "job_description_date",
                }
            )
    return out
