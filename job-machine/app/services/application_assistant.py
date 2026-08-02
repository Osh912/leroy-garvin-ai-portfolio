from __future__ import annotations

"""
Application Assistant — local hiring-process helpers.
Never fabricates companies, salaries, offers, interviews, or checklist truth.
"""

import json
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models import Application, Job
from app.services.cover_letter import generate_cover_letter
from app.services.filters import format_estimated_salary, load_profile, match_reason
from app.services.pipeline_stages import PORTFOLIO_URL, normalize_status, stage_label
from app.services.portfolio_matcher import match_portfolio
from app.services.resume_tailor import tailor_resume
from app.services.scorer import score_job

CHECKLIST_KEYS = [
    "resume_attached",
    "cover_letter_attached",
    "portfolio_url_included",
    "linkedin_included",
    "contact_information_verified",
    "job_requirements_reviewed",
]

CHECKLIST_LABELS = {
    "resume_attached": "Resume attached",
    "cover_letter_attached": "Cover letter attached",
    "portfolio_url_included": "Portfolio URL included",
    "linkedin_included": "LinkedIn included",
    "contact_information_verified": "Contact information verified",
    "job_requirements_reviewed": "Job requirements reviewed",
}


def _parse_meta(row: Application) -> dict[str, Any]:
    try:
        data = json.loads(getattr(row, "analytics_json", None) or "{}")
    except json.JSONDecodeError:
        data = {}
    return data if isinstance(data, dict) else {}


def _save_meta(row: Application, meta: dict[str, Any]) -> None:
    row.analytics_json = json.dumps(meta)


def _candidate() -> dict[str, Any]:
    profile = load_profile()
    return profile.get("candidate") or profile


def default_checklist() -> dict[str, Any]:
    return {k: False for k in CHECKLIST_KEYS}


def default_notes() -> dict[str, str]:
    return {
        "recruiter_name": "",
        "hiring_manager": "",
        "referral": "",
        "interview_notes": "",
        "salary_discussed": "",
        "follow_up_reminders": "",
    }


def default_offer() -> dict[str, Any]:
    return {
        "salary": None,
        "bonus": "",
        "benefits": "",
        "pto": "",
        "remote_policy": "",
        "career_growth": "",
        "overall_score": None,
        "notes": "",
    }


def build_recruiter_summary(
    job: Job,
    *,
    why_match: str,
    projects: list[dict[str, Any]],
    score: float,
) -> str:
    """Truthful one-pager for recruiters from real job + portfolio match only."""
    c = _candidate()
    project_lines = []
    for p in projects[:4]:
        name = p.get("name") or "Project"
        url = p.get("url") or ""
        why = p.get("why") or p.get("reason") or ""
        line = f"- {name}"
        if url:
            line += f" ({url})"
        if why:
            line += f" — {why}"
        project_lines.append(line)
    if not project_lines:
        project_lines = ["- Portfolio: " + (c.get("portfolio") or PORTFOLIO_URL)]

    salary = (job.salary_text or "").strip() or "Not listed on posting"
    return f"""Recruiter Summary — {c.get('full_name', 'Leroy Garvin Jr')}
Role: {job.title} @ {job.company}
Location: {job.location or 'Remote'}
Posted salary: {salary}
Match score (transparent, local): {round(score)}%

Candidate
- Positioning: {c.get('positioning') or 'AI Automation | AI Operations | Workflow Automation'}
- Contact: {c.get('email', '')} · {c.get('phone', '')}
- LinkedIn: {c.get('linkedin', '')}
- Portfolio: {c.get('portfolio') or PORTFOLIO_URL}

Why this role (from Job Machine match)
{why_match or 'No why-match text generated yet.'}

Portfolio evidence to cite
{chr(10).join(project_lines)}

Note: This summary is generated locally from tracked job + portfolio data. Nothing was submitted to the employer.
""".strip()


def compute_checklist_from_materials(
    *,
    resume: str,
    cover: str,
    manual: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Auto-check only what materials actually contain. Never invent completion."""
    c = _candidate()
    portfolio = (c.get("portfolio") or PORTFOLIO_URL).strip()
    linkedin = (c.get("linkedin") or "").strip()
    email = (c.get("email") or "").strip()
    phone = (c.get("phone") or "").strip()
    blob = f"{resume or ''}\n{cover or ''}".lower()

    checklist = default_checklist()
    checklist["resume_attached"] = bool((resume or "").strip())
    checklist["cover_letter_attached"] = bool((cover or "").strip())
    checklist["portfolio_url_included"] = bool(portfolio) and (
        portfolio.lower() in blob or "leroy-garvin-ai-portfolio" in blob
    )
    checklist["linkedin_included"] = bool(linkedin) and (
        linkedin.lower() in blob or "linkedin.com/in/" in blob
    )
    checklist["contact_information_verified"] = bool(email and phone) and (
        email.lower() in blob or phone.replace(" ", "") in blob.replace(" ", "")
    )
    # Requirements review is always Leroy's confirmation
    checklist["job_requirements_reviewed"] = False

    if manual:
        for k in CHECKLIST_KEYS:
            if k in manual and isinstance(manual[k], bool):
                # Allow Leroy to override; auto values are defaults until he edits
                if k == "job_requirements_reviewed" or manual.get("_user_edited"):
                    checklist[k] = manual[k]
                elif k in manual and manual.get("_preserve_user"):
                    checklist[k] = bool(manual[k])
        if "job_requirements_reviewed" in manual:
            checklist["job_requirements_reviewed"] = bool(manual["job_requirements_reviewed"])
        # Preserve explicit user overrides for the first five if flagged
        for k in CHECKLIST_KEYS:
            if k == "job_requirements_reviewed":
                continue
            override_key = f"{k}_override"
            if override_key in manual:
                checklist[k] = bool(manual[override_key])

    checklist["updated_at"] = datetime.utcnow().isoformat() + "Z"
    return checklist


def assistant_bundle(row: Application) -> dict[str, Any]:
    meta = _parse_meta(row)
    notes = {**default_notes(), **(meta.get("application_notes") or {})}
    # Prefer application columns when present
    if row.recruiter_name and not notes.get("recruiter_name"):
        notes["recruiter_name"] = row.recruiter_name
    checklist = meta.get("checklist") or default_checklist()
    for k in CHECKLIST_KEYS:
        checklist.setdefault(k, False)
    offer = {**default_offer(), **(meta.get("offer") or {})}
    return {
        "application_id": row.id,
        "job_id": row.job_id,
        "company": row.company,
        "position": row.position,
        "status": normalize_status(row.status),
        "stage_label": stage_label(row.status),
        "checklist": checklist,
        "checklist_labels": CHECKLIST_LABELS,
        "checklist_complete": all(bool(checklist.get(k)) for k in CHECKLIST_KEYS),
        "application_notes": notes,
        "interview_calendar": meta.get("interview_calendar") or [],
        "lessons_learned": meta.get("lessons_learned") or [],
        "offer": offer,
        "recruiter_summary": meta.get("recruiter_summary") or "",
        "prepared_at": meta.get("prepared_at"),
        "tailored_resume": row.tailored_resume or "",
        "cover_letter": row.cover_letter or "",
        "portfolio_refs": json.loads(row.portfolio_refs or "[]"),
        "portfolio_url": (_candidate().get("portfolio") or PORTFOLIO_URL),
        "linkedin": (_candidate().get("linkedin") or ""),
        "contact": {
            "email": _candidate().get("email") or "",
            "phone": _candidate().get("phone") or "",
            "name": _candidate().get("full_name") or "Leroy Garvin Jr",
        },
        "auto_apply": False,
        "local_only": True,
    }


def _get_or_create_application(job: Job, db: Session) -> Application:
    existing = (
        db.query(Application)
        .filter(Application.job_id == job.id)
        .order_by(Application.updated_at.desc())
        .first()
    )
    if existing:
        return existing
    row = Application(
        job_id=job.id,
        company=job.company,
        position=job.title,
        salary=job.salary_text or "",
        location=job.location or "Remote",
        status="ready",
        notes="Prepared via Application Assistant. Awaiting Leroy approval to apply. Auto-apply: OFF.",
        analytics_json="{}",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def prepare_application(job_id: int, db: Session) -> dict[str, Any]:
    """One-click prepare: resume, cover, portfolio match, recruiter summary + checklist."""
    job = db.get(Job, job_id)
    if not job:
        raise ValueError("Job not found")

    job_dict = {
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "description": job.description,
        "salary_text": job.salary_text,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "is_remote": bool(job.is_remote),
        "tags": job.tags,
        "source": job.source,
    }
    projects = match_portfolio(job_dict)
    score, breakdown = score_job(job_dict)
    why = match_reason(job_dict, projects)
    breakdown["why_match"] = why
    breakdown["estimated_salary"] = format_estimated_salary(job_dict)
    resume, resume_ai, resume_warn = tailor_resume(job_dict, projects)
    cover, cover_ai, cover_warn = generate_cover_letter(job_dict, projects)
    summary = build_recruiter_summary(job, why_match=why, projects=projects, score=score)

    job.score = score
    job.score_breakdown = json.dumps(breakdown)
    job.matched_projects = json.dumps(projects)

    row = _get_or_create_application(job, db)
    meta = _parse_meta(row)
    prev_checklist = meta.get("checklist") or {}
    checklist = compute_checklist_from_materials(resume=resume, cover=cover, manual=prev_checklist)
    # Keep Leroy's requirements review if already checked
    if prev_checklist.get("job_requirements_reviewed"):
        checklist["job_requirements_reviewed"] = True

    meta["checklist"] = checklist
    meta["recruiter_summary"] = summary
    meta["prepared_at"] = datetime.utcnow().isoformat() + "Z"
    meta.setdefault("application_notes", default_notes())
    meta.setdefault("interview_calendar", [])
    meta.setdefault("lessons_learned", [])
    meta.setdefault("offer", default_offer())

    row.tailored_resume = resume
    row.cover_letter = cover
    row.portfolio_refs = json.dumps(projects)
    row.application_score = float(score)
    if row.status in {"saved"}:
        row.status = "ready"
    if why and why not in (row.notes or ""):
        row.notes = ((row.notes or "").strip() + "\n\n" + why).strip()
    _save_meta(row, meta)
    db.add(row)
    db.commit()
    db.refresh(row)

    bundle = assistant_bundle(row)
    bundle.update(
        {
            "match_score": score,
            "why_match": why,
            "used_ai": resume_ai or cover_ai,
            "truth_warnings": list(dict.fromkeys(resume_warn + cover_warn)),
            "score_breakdown": breakdown,
            "fabricated": False,
        }
    )
    return bundle


def update_checklist(app_id: int, updates: dict[str, Any], db: Session) -> dict[str, Any]:
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    meta = _parse_meta(row)
    checklist = meta.get("checklist") or default_checklist()
    for k in CHECKLIST_KEYS:
        if k in updates:
            checklist[k] = bool(updates[k])
            checklist[f"{k}_override"] = bool(updates[k])
    checklist["updated_at"] = datetime.utcnow().isoformat() + "Z"
    meta["checklist"] = checklist
    _save_meta(row, meta)
    db.add(row)
    db.commit()
    db.refresh(row)
    return assistant_bundle(row)


def update_notes(app_id: int, notes_in: dict[str, Any], db: Session) -> dict[str, Any]:
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    meta = _parse_meta(row)
    notes = {**default_notes(), **(meta.get("application_notes") or {})}
    for k in default_notes():
        if k in notes_in and notes_in[k] is not None:
            notes[k] = str(notes_in[k])
    meta["application_notes"] = notes
    # Sync recruiter fields to columns when provided
    if notes.get("recruiter_name"):
        row.recruiter_name = notes["recruiter_name"]
    if notes_in.get("recruiter_email"):
        row.recruiter_email = str(notes_in["recruiter_email"])
    if notes.get("follow_up_reminders") and not row.follow_up_date:
        # leave date alone unless user sets tracker date — store reminder text only
        pass
    _save_meta(row, meta)
    db.add(row)
    db.commit()
    db.refresh(row)
    return assistant_bundle(row)


def upsert_calendar_event(app_id: int, event: dict[str, Any], db: Session) -> dict[str, Any]:
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    meta = _parse_meta(row)
    events: list[dict[str, Any]] = list(meta.get("interview_calendar") or [])
    eid = event.get("id") or str(uuid.uuid4())
    cleaned = {
        "id": eid,
        "date": (event.get("date") or "").strip(),
        "time": (event.get("time") or "").strip(),
        "company": (event.get("company") or row.company or "").strip(),
        "interview_stage": normalize_status(event.get("interview_stage") or event.get("stage") or row.status),
        "meeting_link": (event.get("meeting_link") or "").strip(),
        "interviewers": [
            str(x).strip()
            for x in (event.get("interviewers") or [])
            if str(x).strip()
        ]
        if isinstance(event.get("interviewers"), list)
        else [
            p.strip()
            for p in str(event.get("interviewers") or "").split(",")
            if p.strip()
        ],
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }
    if not cleaned["date"]:
        raise ValueError("Interview date is required")
    replaced = False
    for i, ev in enumerate(events):
        if ev.get("id") == eid:
            events[i] = cleaned
            replaced = True
            break
    if not replaced:
        events.append(cleaned)
    events.sort(key=lambda e: (e.get("date") or "", e.get("time") or ""))
    meta["interview_calendar"] = events
    # Sync primary interview_date column from earliest upcoming/known date
    try:
        from datetime import date as date_cls

        row.interview_date = date_cls.fromisoformat(cleaned["date"][:10])
    except ValueError:
        pass
    _save_meta(row, meta)
    db.add(row)
    db.commit()
    db.refresh(row)
    return assistant_bundle(row)


def delete_calendar_event(app_id: int, event_id: str, db: Session) -> dict[str, Any]:
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    meta = _parse_meta(row)
    events = [e for e in (meta.get("interview_calendar") or []) if e.get("id") != event_id]
    meta["interview_calendar"] = events
    _save_meta(row, meta)
    db.add(row)
    db.commit()
    db.refresh(row)
    return assistant_bundle(row)


def add_lesson(app_id: int, lesson: dict[str, Any], db: Session) -> dict[str, Any]:
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    meta = _parse_meta(row)
    lessons: list[dict[str, Any]] = list(meta.get("lessons_learned") or [])
    entry = {
        "id": lesson.get("id") or str(uuid.uuid4()),
        "interview_date": (lesson.get("interview_date") or "").strip(),
        "stage": normalize_status(lesson.get("stage") or row.status),
        "what_went_well": (lesson.get("what_went_well") or "").strip(),
        "what_to_improve": (lesson.get("what_to_improve") or "").strip(),
        "questions_asked": [
            str(q).strip()
            for q in (lesson.get("questions_asked") or [])
            if str(q).strip()
        ]
        if isinstance(lesson.get("questions_asked"), list)
        else [
            q.strip()
            for q in str(lesson.get("questions_asked") or "").split("\n")
            if q.strip()
        ],
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    if not entry["what_went_well"] and not entry["what_to_improve"] and not entry["questions_asked"]:
        raise ValueError("Add at least one lesson field (what went well, improve, or questions).")
    # Upsert by id
    found = False
    for i, L in enumerate(lessons):
        if L.get("id") == entry["id"]:
            lessons[i] = entry
            found = True
            break
    if not found:
        lessons.insert(0, entry)
    meta["lessons_learned"] = lessons

    # Feed interview analytics for Recruiter Analytics (real logged data only)
    ia = meta.get("interview_analytics") or {}
    if not isinstance(ia, dict):
        ia = {}
    qs = list(ia.get("questions_asked") or [])
    for q in entry["questions_asked"]:
        if q not in qs:
            qs.append(q)
    ia["questions_asked"] = qs[:50]
    if entry["what_to_improve"]:
        weak = list(ia.get("weak_topics") or [])
        if entry["what_to_improve"] not in weak:
            weak.append(entry["what_to_improve"])
        ia["weak_topics"] = weak[:20]
    if entry["what_went_well"]:
        strong = list(ia.get("strong_topics") or [])
        if entry["what_went_well"] not in strong:
            strong.append(entry["what_went_well"])
        ia["strong_topics"] = strong[:20]
    meta["interview_analytics"] = ia

    _save_meta(row, meta)
    db.add(row)
    db.commit()
    db.refresh(row)
    return assistant_bundle(row)


def update_offer(app_id: int, offer_in: dict[str, Any], db: Session) -> dict[str, Any]:
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    meta = _parse_meta(row)
    offer = {**default_offer(), **(meta.get("offer") or {})}
    for k in default_offer():
        if k in offer_in:
            offer[k] = offer_in[k]
    # Coerce numeric fields when provided
    if offer.get("salary") in ("", None):
        offer["salary"] = None
    else:
        try:
            offer["salary"] = float(offer["salary"])
        except (TypeError, ValueError):
            # Keep as string only if user typed non-numeric — store text in notes instead
            if isinstance(offer.get("salary"), str):
                offer["notes"] = ((offer.get("notes") or "") + f"\nSalary text: {offer['salary']}").strip()
            offer["salary"] = None
    if offer.get("overall_score") in ("", None):
        offer["overall_score"] = None
    else:
        try:
            offer["overall_score"] = float(offer["overall_score"])
        except (TypeError, ValueError):
            offer["overall_score"] = None
    meta["offer"] = offer
    _save_meta(row, meta)
    if normalize_status(row.status) not in {"offer", "accepted", "rejected", "withdrawn"}:
        # Do not auto-move stage — Leroy controls tracker; only store offer data
        pass
    db.add(row)
    db.commit()
    db.refresh(row)
    return assistant_bundle(row)


def list_calendar(db: Session) -> list[dict[str, Any]]:
    rows = db.query(Application).order_by(Application.updated_at.desc()).all()
    out: list[dict[str, Any]] = []
    for row in rows:
        meta = _parse_meta(row)
        for ev in meta.get("interview_calendar") or []:
            out.append(
                {
                    **ev,
                    "application_id": row.id,
                    "job_id": row.job_id,
                    "position": row.position,
                    "stage_label": stage_label(ev.get("interview_stage") or row.status),
                }
            )
    out.sort(key=lambda e: (e.get("date") or "", e.get("time") or ""))
    return out


def list_lessons(db: Session) -> list[dict[str, Any]]:
    rows = db.query(Application).order_by(Application.updated_at.desc()).all()
    out: list[dict[str, Any]] = []
    for row in rows:
        meta = _parse_meta(row)
        for lesson in meta.get("lessons_learned") or []:
            out.append(
                {
                    **lesson,
                    "application_id": row.id,
                    "company": row.company,
                    "position": row.position,
                }
            )
    out.sort(key=lambda x: x.get("created_at") or "", reverse=True)
    return out


def compare_offers(db: Session) -> dict[str, Any]:
    """Compare only offers Leroy has entered — never invent compensation."""
    rows = db.query(Application).order_by(Application.updated_at.desc()).all()
    offers = []
    for row in rows:
        meta = _parse_meta(row)
        offer = meta.get("offer") or {}
        has_data = any(
            [
                offer.get("salary") is not None,
                bool(offer.get("bonus")),
                bool(offer.get("benefits")),
                bool(offer.get("pto")),
                bool(offer.get("remote_policy")),
                bool(offer.get("career_growth")),
                offer.get("overall_score") is not None,
            ]
        )
        if not has_data and normalize_status(row.status) not in {"offer", "accepted"}:
            continue
        if not has_data:
            continue
        offers.append(
            {
                "application_id": row.id,
                "company": row.company,
                "position": row.position,
                "status": normalize_status(row.status),
                "stage_label": stage_label(row.status),
                "salary": offer.get("salary"),
                "bonus": offer.get("bonus") or "",
                "benefits": offer.get("benefits") or "",
                "pto": offer.get("pto") or "",
                "remote_policy": offer.get("remote_policy") or "",
                "career_growth": offer.get("career_growth") or "",
                "overall_score": offer.get("overall_score"),
                "notes": offer.get("notes") or "",
            }
        )
    offers.sort(
        key=lambda o: (
            o["overall_score"] is not None,
            o["overall_score"] or 0,
            o["salary"] or 0,
        ),
        reverse=True,
    )
    return {
        "offers": offers,
        "count": len(offers),
        "fabricated": False,
        "local_only": True,
        "note": "Offer rows appear only after you enter offer details on an application. Empty fields mean not recorded — not estimated.",
    }


def assistant_overview(db: Session) -> dict[str, Any]:
    apps = db.query(Application).order_by(Application.updated_at.desc()).all()
    ready = [assistant_bundle(a) for a in apps[:40]]
    return {
        "mode": "application_assistant",
        "fabricated": False,
        "local_only": True,
        "auto_apply": False,
        "applications": ready,
        "calendar": list_calendar(db),
        "lessons": list_lessons(db),
        "offers": compare_offers(db),
        "checklist_labels": CHECKLIST_LABELS,
        "contact": {
            "email": _candidate().get("email") or "",
            "phone": _candidate().get("phone") or "",
            "linkedin": _candidate().get("linkedin") or "",
            "portfolio": _candidate().get("portfolio") or PORTFOLIO_URL,
            "name": _candidate().get("full_name") or "Leroy Garvin Jr",
        },
    }
