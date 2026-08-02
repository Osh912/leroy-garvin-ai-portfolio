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


async def run_career_agent_morning(db: Session, *, prepare_packets: bool = True) -> dict[str, Any]:
    """
    8:00 AM autonomous run:
    search boards → purge expired/unverified → score → packets → Daily Brief.
    Never auto-submits. Never sends email.
    """
    from app.services.interview_pipeline import morning_refresh

    refresh_log = await morning_refresh(db, prepare_packets=prepare_packets)
    brief = build_daily_brief(db, refresh_log=refresh_log)
    save_daily_brief(brief)
    AGENT_LAST.parent.mkdir(parents=True, exist_ok=True)
    AGENT_LAST.write_text(json.dumps({"ran_at": brief["generated_at"], "brief_date": brief["date"]}, indent=2), encoding="utf-8")
    return {
        "ok": True,
        "mode": "ai_career_agent",
        "auto_apply": False,
        "auto_email": False,
        "approval_required": True,
        "refresh": refresh_log,
        "brief": brief,
        "notifications": brief.get("notifications") or [],
    }


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
