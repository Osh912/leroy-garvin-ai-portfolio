from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(prefix="/api/career-agent", tags=["career-agent"])


@router.get("/status")
def career_agent_status():
    from app.services.career_agent import AGENT_LAST, load_latest_brief

    last = None
    if AGENT_LAST.exists():
        import json

        try:
            last = json.loads(AGENT_LAST.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            last = None
    return {
        "mode": "ai_career_agent_2_0",
        "auto_apply": False,
        "auto_email": False,
        "approval_required": True,
        "notify_threshold": 80,
        "alert_threshold": 90,
        "run_now_available": True,
        "last_run": last,
        "has_brief": load_latest_brief() is not None,
        "scoring_mode": "transparent_match_score_v2",
    }


@router.post("/run-morning")
async def run_morning(prepare_packets: bool = True, db: Session = Depends(get_db)):
    from app.services.career_agent import run_career_agent_morning

    return await run_career_agent_morning(
        db, prepare_packets=prepare_packets, force=False, trigger="api_morning"
    )


@router.post("/run-now")
async def run_now_endpoint(prepare_packets: bool = True, db: Session = Depends(get_db)):
    """Manual RUN NOW — full agent pipeline without waiting for 8:00 AM."""
    from app.services.career_agent import run_now

    return await run_now(db, prepare_packets=prepare_packets)


@router.get("/todays-brief")
def todays_brief(db: Session = Depends(get_db)):
    from app.services.career_agent import build_todays_brief, load_latest_brief

    latest = load_latest_brief()
    if latest and latest.get("todays_brief"):
        return latest["todays_brief"]
    return build_todays_brief(db, refresh_log=None, analytics=None)


@router.get("/daily-brief")
def daily_brief(rebuild: bool = False, db: Session = Depends(get_db)):
    from app.services.career_agent import build_daily_brief, load_latest_brief, save_daily_brief

    if not rebuild:
        existing = load_latest_brief()
        if existing:
            return existing
    brief = build_daily_brief(db, refresh_log=None)
    save_daily_brief(brief)
    return brief


@router.get("/coach")
def career_coach(db: Session = Depends(get_db)):
    from app.services.career_coach import analyze_career

    return analyze_career(db)


@router.post("/coach/weekly-report")
def weekly_report(db: Session = Depends(get_db)):
    from app.services.career_coach import weekly_improvement_report

    return weekly_improvement_report(db)


@router.get("/coach/weekly-report")
def weekly_report_latest(db: Session = Depends(get_db)):
    from app.services.career_coach import load_latest_weekly_report, weekly_improvement_report

    existing = load_latest_weekly_report()
    if existing:
        return existing
    return weekly_improvement_report(db)


@router.get("/crm")
def crm_list(db: Session = Depends(get_db)):
    from app.services.recruiter_crm import list_contacts

    return {"contacts": list_contacts(db), "auto_email": False, "fabricated": False}


@router.post("/crm")
def crm_create(payload: dict, db: Session = Depends(get_db)):
    from app.services.recruiter_crm import upsert_contact

    return upsert_contact(db, payload or {})


@router.patch("/crm/{contact_id}")
def crm_update(contact_id: int, payload: dict, db: Session = Depends(get_db)):
    from app.services.recruiter_crm import upsert_contact

    try:
        return upsert_contact(db, payload or {}, contact_id=contact_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.delete("/crm/{contact_id}")
def crm_delete(contact_id: int, db: Session = Depends(get_db)):
    from app.services.recruiter_crm import delete_contact

    if not delete_contact(db, contact_id):
        raise HTTPException(404, "Recruiter contact not found")
    return {"deleted": True, "id": contact_id}


@router.post("/crm/import-from-applications")
def crm_import(db: Session = Depends(get_db)):
    from app.services.recruiter_crm import import_from_applications

    return import_from_applications(db)


@router.get("/crm/followups")
def crm_followups(db: Session = Depends(get_db)):
    from app.services.recruiter_crm import followups_due

    return {"followups": followups_due(db), "auto_email": False, "approval_required": True}


@router.get("/interview-intelligence")
def interview_intel(
    application_id: int | None = Query(None),
    job_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    from app.services.interview_intelligence import generate_interview_intelligence

    if application_id is None and job_id is None:
        raise HTTPException(400, "Provide application_id or job_id")
    try:
        return generate_interview_intelligence(application_id, job_id, db)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.post("/interview-intelligence")
def interview_intel_post(payload: dict, db: Session = Depends(get_db)):
    from app.services.interview_intelligence import generate_interview_intelligence

    try:
        return generate_interview_intelligence(
            (payload or {}).get("application_id"),
            (payload or {}).get("job_id"),
            db,
        )
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
