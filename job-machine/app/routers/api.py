from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Application, Job
from app.schemas import (
    ApplicationIn,
    ApplicationOut,
    ApplicationUpdate,
    DashboardOut,
    ExportOut,
    GenerateOut,
    HighestInterviewOut,
    InterviewPrepOut,
    JobOut,
    ManualJobIn,
)
from app.services.cover_letter import generate_cover_letter
from app.services.filters import level_hint
from app.services.job_finder import purge_unverified_remote, search_jobs, upsert_jobs
from app.services.pipeline_stages import PORTFOLIO_URL, PIPELINE_STAGES, is_valid_status, stage_label
from app.services.portfolio_matcher import match_portfolio
from app.services.resume_tailor import tailor_resume
from app.services.scorer import score_job

router = APIRouter(prefix="/api")


def _job_out(job: Job, *, rank: int | None = None, is_top_10: bool = False, package_ready: bool = False) -> JobOut:
    breakdown = json.loads(job.score_breakdown or "{}")
    projects = json.loads(job.matched_projects or "[]")
    from app.services.filters import verify_remote
    from app.services.production import careers_url_for_job, source_display

    verification = breakdown.get("remote_verification") or verify_remote(
        {
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "description": job.description or "",
            "tags": job.tags or "",
            "source": job.source,
            "url": job.url,
        }
    )
    careers = breakdown.get("careers_url") or careers_url_for_job(
        {"source": job.source, "url": job.url, "company": job.company}
    )
    active = breakdown.get("active_check") or {}
    est = (
        breakdown.get("estimated_salary")
        or job.salary_text
        or (
            f"${job.salary_min:,.0f} – ${job.salary_max:,.0f}"
            if job.salary_min and job.salary_max
            else job.salary_text or "Not listed"
        )
    )
    match_score = float(breakdown.get("match_score") or breakdown.get("match_percentage") or job.score or 0)
    return JobOut(
        id=job.id,
        external_id=job.external_id,
        source=job.source,
        source_display=str(breakdown.get("source_display") or source_display(job.source)),
        company=job.company,
        title=job.title,
        location=job.location,
        is_remote=bool(job.is_remote) and bool(verification.get("verified")),
        remote_verified=bool(verification.get("verified")),
        remote_verified_label=str(verification.get("label") or "✗ Not Verified Remote"),
        salary_text=job.salary_text,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        url=job.url,
        posting_url=job.url,
        careers_url=str(careers or ""),
        description=job.description,
        tags=job.tags,
        level_hint=job.level_hint,
        score=job.score,
        match_score=match_score,
        match_percentage=match_score,
        interview_probability=None,
        estimated_salary=str(est),
        why_match=str(breakdown.get("why_match") or ""),
        score_breakdown=breakdown,
        matched_projects=projects,
        found_at=job.found_at,
        date_found=job.found_at.isoformat() + "Z" if job.found_at else "",
        last_verified_at=active.get("checked_at"),
        is_active=bool(active.get("active", True)) if active else True,
        package_ready=package_ready,
        posted_at=job.posted_at,
        status=job.status,
        rank=rank,
        is_top_10=is_top_10,
    )



def _app_out(row: Application) -> ApplicationOut:
    try:
        prep = json.loads(getattr(row, "interview_prep", None) or "{}")
    except json.JSONDecodeError:
        prep = {}
    try:
        analytics = json.loads(getattr(row, "analytics_json", None) or "{}")
    except json.JSONDecodeError:
        analytics = {}
    ip = float(row.application_score or 0)
    return ApplicationOut(
        id=row.id,
        job_id=row.job_id,
        company=row.company,
        position=row.position,
        salary=row.salary,
        location=row.location,
        date_applied=row.date_applied,
        status=row.status,
        stage_label=stage_label(row.status),
        follow_up_date=row.follow_up_date,
        interview_date=row.interview_date,
        notes=row.notes,
        recruiter_name=row.recruiter_name,
        recruiter_email=row.recruiter_email,
        tailored_resume=row.tailored_resume,
        cover_letter=row.cover_letter,
        interview_prep=prep if isinstance(prep, dict) else {},
        analytics=analytics if isinstance(analytics, dict) else {},
        portfolio_refs=json.loads(row.portfolio_refs or "[]"),
        application_score=row.application_score,
        interview_probability=ip,
        portfolio_url=PORTFOLIO_URL,
        approval_required=row.status in {"saved", "ready"},
        created_at=row.created_at,
        updated_at=row.updated_at,
    )



@router.post("/jobs/search")
async def api_search_jobs(
    persist: bool = True,
    strict_level: bool = True,
    fully_remote_only: bool = True,
    us_only: bool = True,
    min_salary: float = Query(60000, ge=0),
    prefer_no_degree: bool = True,
    block_five_plus_years: bool = True,
    require_salary_listed: bool = False,
    verify_active: bool = True,
    quick_filters: str = Query("", description="Comma-separated quick filter labels"),
    db: Session = Depends(get_db),
):
    from app.services.job_finder import purge_placeholders

    qf = [x.strip() for x in quick_filters.split(",") if x.strip()]
    purged = purge_placeholders(db)
    result = await search_jobs(
        strict_level=strict_level,
        fully_remote_only=fully_remote_only,
        us_only=us_only,
        min_salary=min_salary,
        prefer_no_degree=prefer_no_degree,
        block_five_plus_years=block_five_plus_years,
        quick_filters=qf or None,
        require_salary_listed=require_salary_listed,
        verify_active=verify_active,
    )
    added = 0
    remote_purged = 0
    if persist:
        remote_purged = purge_unverified_remote(db)
        added = upsert_jobs(db, result["jobs"])
    top = result["jobs"][:10]
    return {
        "fetched": result["fetched"],
        "matched": result["matched"],
        "added": added,
        "purged_placeholders": purged,
        "purged_unverified_remote": remote_purged,
        "rejected_unverified_remote": result.get("rejected_unverified_remote", 0),
        "rejected_inactive": result.get("rejected_inactive", 0),
        "rejected_placeholder": result.get("rejected_placeholder", 0),
        "errors": result["errors"],
        "sources_note": result["sources_note"],
        "ranking_mode": result.get("ranking_mode"),
        "remote_mode": result.get("remote_mode"),
        "production_mode": True,
        "refreshed_at": result.get("refreshed_at"),
        "weights": result.get("weights"),
        "filters_applied": result.get("filters_applied"),
        "top_10": top,
        "jobs": result["jobs"][:100],
        "auto_apply": False,
    }



@router.get("/jobs", response_model=list[JobOut])
def list_jobs(
    q: str = "",
    min_score: float = Query(0, ge=0, le=100),
    status: str = "",
    quick_filters: str = "",
    verified_remote_only: bool = True,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    from app.services.filters import matches_quick_filters, verify_remote

    query = db.query(Job).filter(
        ~Job.status.in_(
            ["hidden-unverified-remote", "hidden-placeholder", "hidden-inactive"]
        )
    )
    if status:
        query = query.filter(Job.status == status)
    if min_score:
        query = query.filter(Job.score >= min_score)
    if q:
        like = f"%{q}%"
        query = query.filter(
            (Job.title.ilike(like)) | (Job.company.ilike(like)) | (Job.tags.ilike(like))
        )
    rows = query.order_by(Job.score.desc(), Job.found_at.desc()).limit(limit * 4).all()
    qf = [x.strip() for x in quick_filters.split(",") if x.strip()]
    ready_ids = {
        a.job_id
        for a in db.query(Application).filter(Application.status.in_(["ready", "applied"])).all()
        if a.job_id
    }
    out: list[JobOut] = []
    from app.services.production import is_placeholder_company, is_production_eligible

    for r in rows:
        if is_placeholder_company(r.company):
            continue
        job_dict = {
            "title": r.title,
            "company": r.company,
            "location": r.location,
            "description": r.description,
            "tags": r.tags,
            "is_remote": bool(r.is_remote),
            "source": r.source,
            "url": r.url,
        }
        if not is_production_eligible(job_dict)[0]:
            continue
        if verified_remote_only and not verify_remote(job_dict)["verified"]:
            continue
        if qf and not matches_quick_filters(job_dict, qf):
            continue
        out.append(_job_out(r, package_ready=r.id in ready_ids))
        if len(out) >= limit * 2:
            break
    # Production: rank by transparent Match Score
    out.sort(key=lambda j: (j.match_score, j.match_percentage), reverse=True)
    ranked: list[JobOut] = []
    for i, j in enumerate(out[:limit]):
        j.rank = i + 1 if i < 10 else None
        j.is_top_10 = i < 10
        ranked.append(j)
    return ranked


@router.get("/jobs/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return _job_out(job)


@router.post("/jobs/manual", response_model=JobOut)
def manual_job(payload: ManualJobIn, db: Session = Depends(get_db)):
    from app.services.production import is_placeholder_company, is_production_eligible

    if is_placeholder_company(payload.company):
        raise HTTPException(400, "Placeholder / demo companies are blocked in Production Mode.")
    job_dict = {
        "external_id": f"manual-{datetime.utcnow().timestamp()}",
        "source": payload.source or "manual",
        "company": payload.company,
        "title": payload.title,
        "location": payload.location,
        "url": payload.url,
        "description": payload.description,
        "salary_text": payload.salary_text,
        "is_remote": True,
        "tags": [],
    }
    ok, reason = is_production_eligible(job_dict)
    if not ok:
        raise HTTPException(400, f"Job rejected ({reason}). Provide a real company and official posting URL.")
    from app.services.filters import parse_salary

    smin, smax = parse_salary(payload.salary_text)
    job_dict["salary_min"] = smin
    job_dict["salary_max"] = smax
    job_dict["level_hint"] = level_hint(job_dict)
    score, breakdown = score_job(job_dict)
    projects = match_portfolio(job_dict)
    from app.services.filters import format_estimated_salary, match_reason

    why = match_reason(job_dict, projects)
    breakdown["why_match"] = why
    breakdown["estimated_salary"] = format_estimated_salary(job_dict)
    breakdown["portfolio_to_cite"] = [p.get("name") for p in projects[:4]]
    row = Job(
        external_id=job_dict["external_id"],
        source=job_dict["source"],
        company=payload.company,
        title=payload.title,
        location=payload.location,
        is_remote=1,
        salary_text=payload.salary_text,
        salary_min=smin,
        salary_max=smax,
        url=payload.url,
        description=payload.description,
        tags="",
        level_hint=job_dict["level_hint"],
        score=score,
        score_breakdown=json.dumps(breakdown),
        matched_projects=json.dumps(projects),
        status="new",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _job_out(row)


@router.post("/jobs/{job_id}/generate", response_model=GenerateOut)
def generate_packet(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    from app.services.filters import format_estimated_salary, match_reason

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
    job.score = score
    job.score_breakdown = json.dumps(breakdown)
    job.matched_projects = json.dumps(projects)
    db.commit()
    return GenerateOut(
        job_id=job.id,
        score=score,
        score_breakdown=breakdown,
        matched_projects=projects,
        tailored_resume=resume,
        cover_letter=cover,
        why_match=why,
        interview_probability=float(breakdown.get("interview_probability") or 0),
        used_ai=resume_ai or cover_ai,
        truth_warnings=list(dict.fromkeys(resume_warn + cover_warn)),
        auto_apply=False,
        approval_required=True,
    )


@router.get("/applications", response_model=list[ApplicationOut])
def list_applications(db: Session = Depends(get_db)):
    rows = db.query(Application).order_by(Application.updated_at.desc()).all()
    return [_app_out(r) for r in rows]


@router.post("/applications", response_model=ApplicationOut)
def create_application(payload: ApplicationIn, db: Session = Depends(get_db)):
    row = Application(
        job_id=payload.job_id or 0,
        company=payload.company,
        position=payload.position,
        salary=payload.salary,
        location=payload.location,
        date_applied=payload.date_applied,
        status=payload.status,
        follow_up_date=payload.follow_up_date,
        interview_date=payload.interview_date,
        notes=payload.notes,
        recruiter_name=payload.recruiter_name,
        recruiter_email=payload.recruiter_email,
        tailored_resume=payload.tailored_resume,
        cover_letter=payload.cover_letter,
        portfolio_refs=json.dumps(payload.portfolio_refs),
        application_score=payload.application_score,
    )
    db.add(row)
    if payload.job_id:
        job = db.get(Job, payload.job_id)
        if job:
            job.status = payload.status if payload.status != "saved" else "tracking"
    db.commit()
    db.refresh(row)
    return _app_out(row)


@router.patch("/applications/{app_id}", response_model=ApplicationOut)
def update_application(app_id: int, payload: ApplicationUpdate, db: Session = Depends(get_db)):
    row = db.get(Application, app_id)
    if not row:
        raise HTTPException(404, "Application not found")
    data = payload.model_dump(exclude_unset=True)
    if "portfolio_refs" in data and data["portfolio_refs"] is not None:
        data["portfolio_refs"] = json.dumps(data["portfolio_refs"])
    if "interview_prep" in data and data["interview_prep"] is not None:
        data["interview_prep"] = json.dumps(data["interview_prep"])
    if "analytics" in data and data["analytics"] is not None:
        # merge into analytics_json
        try:
            existing = json.loads(getattr(row, "analytics_json", None) or "{}")
        except json.JSONDecodeError:
            existing = {}
        if not isinstance(existing, dict):
            existing = {}
        existing.update(data.pop("analytics") or {})
        data["analytics_json"] = json.dumps(existing)
    if "status" in data and data["status"] == "applied" and row.status != "applied":
        raise HTTPException(
            400,
            "Use POST /api/applications/{id}/approve to mark Applied. Auto-apply is disabled.",
        )
    if "status" in data and data["status"] is not None and not is_valid_status(data["status"]):
        raise HTTPException(400, f"Invalid stage. Use one of: {', '.join(PIPELINE_STAGES)}")
    for k, v in data.items():
        setattr(row, k, v)
    row.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(row)
    return _app_out(row)


@router.post("/applications/from-job/{job_id}", response_model=ApplicationOut)
def track_from_job(job_id: int, status: str = "ready", db: Session = Depends(get_db)):
    """Create tracker entry. Default status is 'ready' — never auto-applies."""
    if status == "applied":
        raise HTTPException(
            400,
            "Cannot auto-apply. Create as 'ready' or 'saved', then POST /api/applications/{id}/approve.",
        )
    if status not in PIPELINE_STAGES and not is_valid_status(status):
        raise HTTPException(400, f"Invalid stage. Use one of: {', '.join(PIPELINE_STAGES)}")
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    gen = generate_packet(job_id, db)
    row = Application(
        job_id=job.id,
        company=job.company,
        position=job.title,
        salary=job.salary_text,
        location=job.location,
        date_applied=None,
        status=status if status != "applied" else "ready",
        tailored_resume=gen.tailored_resume,
        cover_letter=gen.cover_letter,
        portfolio_refs=json.dumps(gen.matched_projects),
        application_score=gen.score,
        notes="Created from Interview Pipeline. Awaiting Leroy approval to apply. Auto-apply: OFF.",
    )
    job.status = row.status
    db.add(row)
    db.commit()
    db.refresh(row)
    return _app_out(row)


@router.get("/dashboard", response_model=DashboardOut)
def dashboard(db: Session = Depends(get_db)):
    today = date.today()
    start = datetime(today.year, today.month, today.day)
    new_jobs_today = db.query(Job).filter(Job.found_at >= start).count()
    apps = db.query(Application).all()
    applications_ready = sum(1 for a in apps if a.status == "ready")
    applications_sent = sum(
        1
        for a in apps
        if a.status
        in {
            "applied",
            "recruiter_contact",
            "first_interview",
            "technical_interview",
            "final_interview",
            "offer",
        }
    )
    interviews_scheduled = sum(
        1
        for a in apps
        if a.interview_date
        or a.status in {"first_interview", "technical_interview", "final_interview", "recruiter_contact"}
    )
    interviews = interviews_scheduled
    follow_ups_due = sum(
        1
        for a in apps
        if a.follow_up_date and a.follow_up_date <= today and a.status not in {"rejected", "offer"}
    )

    from app.services.interview_pipeline import (
        highest_probability_this_week,
        rank_jobs_by_interview_probability,
    )
    from app.services.job_finder import read_last_refresh

    best = rank_jobs_by_interview_probability(db, limit=10)
    ready_ids = {
        a.job_id
        for a in db.query(Application).filter(Application.status.in_(["ready", "applied"])).all()
        if a.job_id
    }
    recent = db.query(Application).order_by(Application.updated_at.desc()).limit(10).all()
    status_counts: dict[str, int] = {}
    for a in apps:
        status_counts[a.status] = status_counts.get(a.status, 0) + 1

    highest = highest_probability_this_week(db)
    highest_out = HighestInterviewOut(**highest) if highest else None
    last = read_last_refresh()

    return DashboardOut(
        new_jobs_today=new_jobs_today,
        applications_ready=applications_ready,
        applications_sent=applications_sent,
        interviews_scheduled=interviews_scheduled,
        interviews=interviews,
        follow_ups_due=follow_ups_due,
        highest_probability_interview_this_week=highest_out,
        best_new_opportunities=[
            _job_out(j, rank=i + 1, is_top_10=True, package_ready=j.id in ready_ids)
            for i, j in enumerate(best)
        ],
        recent_applications=[_app_out(a) for a in recent],
        status_counts=status_counts,
        auto_apply=False,
        mode="production",
        last_refresh=last,
        refreshed_at=(last or {}).get("refreshed_at"),
    )


@router.get("/profile")
def profile():
    from app.services.filters import load_portfolio, load_profile

    return {"profile": load_profile(), "portfolio": load_portfolio()}


@router.get("/pipeline/stages")
def pipeline_stages():
    return {"stages": PIPELINE_STAGES, "labels": {s: stage_label(s) for s in PIPELINE_STAGES}, "auto_apply": False}


@router.post("/pipeline/morning-refresh")
async def api_morning_refresh(
    prepare_packets: bool = True,
    db: Session = Depends(get_db),
):
    from app.services.interview_pipeline import morning_refresh

    return await morning_refresh(db, prepare_packets=prepare_packets)


@router.post("/pipeline/prepare-top10")
def api_prepare_top10(db: Session = Depends(get_db)):
    from app.services.interview_pipeline import prepare_top_packets

    packets = prepare_top_packets(db, limit=10)
    return {"prepared": len(packets), "auto_apply": False, "packets": packets}


@router.post("/jobs/{job_id}/interview-prep", response_model=InterviewPrepOut)
def api_interview_prep(job_id: int, db: Session = Depends(get_db)):
    from app.services.filters import match_reason
    from app.services.interview_prep import build_interview_prep, render_prep_markdown
    from app.services.packet_store import save_packet_locally

    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    job_dict = {
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "description": job.description,
        "salary_text": job.salary_text,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "tags": job.tags,
        "source": job.source,
    }
    projects = match_portfolio(job_dict)
    why = match_reason(job_dict, projects)
    gen = generate_packet(job_id, db)
    prep = build_interview_prep(job_dict, projects, why_match=why)
    paths = save_packet_locally(
        job_id=job.id,
        company=job.company,
        title=job.title,
        resume=gen.tailored_resume,
        cover=gen.cover_letter,
        prep=prep,
        projects=projects,
        why_match=why,
        interview_probability=gen.interview_probability,
        match_percentage=gen.score,
        estimated_salary=str((gen.score_breakdown or {}).get("estimated_salary") or job.salary_text or "Not listed"),
        status="ready",
    )
    app = (
        db.query(Application)
        .filter(Application.job_id == job.id)
        .order_by(Application.updated_at.desc())
        .first()
    )
    if app:
        app.interview_prep = json.dumps(prep)
        app.tailored_resume = gen.tailored_resume
        app.cover_letter = gen.cover_letter
        app.portfolio_refs = json.dumps(projects)
        if app.status in {"saved", ""}:
            app.status = "ready"
        app.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(app)
    return InterviewPrepOut(
        job_id=job.id,
        application_id=app.id if app else None,
        company=job.company,
        title=job.title,
        prep=prep,
        prep_markdown=render_prep_markdown(prep, job_dict),
        packet_paths=paths,
        auto_apply=False,
    )


@router.post("/applications/{app_id}/approve", response_model=ApplicationOut)
def approve_apply(app_id: int, db: Session = Depends(get_db)):
    """Leroy's explicit approval — the only way to mark Applied."""
    from app.services.interview_pipeline import approve_application

    try:
        row = approve_application(db, app_id)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    return _app_out(row)


@router.get("/applications/{app_id}/export", response_model=ExportOut)
def export_application(app_id: int, db: Session = Depends(get_db)):
    from app.services.packet_store import export_bundle_files

    row = db.get(Application, app_id)
    if not row:
        raise HTTPException(404, "Application not found")
    bundle = export_bundle_files(
        resume=row.tailored_resume or "# Resume not generated yet",
        cover=row.cover_letter or "# Cover letter not generated yet",
        portfolio_url=PORTFOLIO_URL,
        company=row.company,
        title=row.position,
        job_id=row.job_id,
        application_id=row.id,
    )
    return ExportOut(application_id=row.id, job_id=row.job_id, **bundle)


@router.get("/jobs/{job_id}/export", response_model=ExportOut)
def export_job(job_id: int, db: Session = Depends(get_db)):
    from app.services.packet_store import export_bundle_files

    gen = generate_packet(job_id, db)
    job = db.get(Job, job_id)
    bundle = export_bundle_files(
        resume=gen.tailored_resume,
        cover=gen.cover_letter,
        portfolio_url=PORTFOLIO_URL,
        company=job.company if job else "company",
        title=job.title if job else "role",
        job_id=job_id,
    )
    return ExportOut(job_id=job_id, **bundle)


def _resolve_export_folder(company: str, title: str, job_id: int | None, application_id: int | None):
    from app.services.packet_store import packet_dir

    folder_id = job_id if job_id is not None else (application_id or 0)
    return packet_dir(folder_id, company, title)


@router.get("/applications/{app_id}/export/zip")
def export_application_zip(app_id: int, db: Session = Depends(get_db)):
    from fastapi.responses import FileResponse

    from app.services.document_export import build_packet_zip
    from app.services.packet_store import export_bundle_files

    row = db.get(Application, app_id)
    if not row:
        raise HTTPException(404, "Application not found")
    bundle = export_bundle_files(
        resume=row.tailored_resume or "",
        cover=row.cover_letter or "",
        portfolio_url=PORTFOLIO_URL,
        company=row.company,
        title=row.position,
        job_id=row.job_id,
        application_id=row.id,
    )
    folder = Path(bundle["folder"])
    zip_path = build_packet_zip(folder)
    return FileResponse(
        path=str(zip_path),
        media_type="application/zip",
        filename=f"{row.company}_{row.position}_packet.zip".replace(" ", "-"),
    )


@router.get("/jobs/{job_id}/export/zip")
def export_job_zip(job_id: int, db: Session = Depends(get_db)):
    from fastapi.responses import FileResponse

    from app.services.document_export import build_packet_zip
    from app.services.packet_store import export_bundle_files

    gen = generate_packet(job_id, db)
    job = db.get(Job, job_id)
    company = job.company if job else "company"
    title = job.title if job else "role"
    bundle = export_bundle_files(
        resume=gen.tailored_resume,
        cover=gen.cover_letter,
        portfolio_url=PORTFOLIO_URL,
        company=company,
        title=title,
        job_id=job_id,
    )
    zip_path = build_packet_zip(Path(bundle["folder"]))
    return FileResponse(
        path=str(zip_path),
        media_type="application/zip",
        filename=f"{company}_{title}_packet.zip".replace(" ", "-"),
    )


@router.get("/applications/{app_id}/export/file/{filename}")
def export_application_file(app_id: int, filename: str, db: Session = Depends(get_db)):
    from fastapi.responses import FileResponse

    from app.services.document_export import is_standard_packet_filename
    from app.services.packet_store import export_bundle_files

    row = db.get(Application, app_id)
    if not row:
        raise HTTPException(404, "Application not found")
    if not is_standard_packet_filename(filename):
        raise HTTPException(400, "Invalid export filename")
    bundle = export_bundle_files(
        resume=row.tailored_resume or "",
        cover=row.cover_letter or "",
        portfolio_url=PORTFOLIO_URL,
        company=row.company,
        title=row.position,
        job_id=row.job_id,
        application_id=row.id,
    )
    path = Path(bundle["folder"]) / filename
    if not path.exists():
        raise HTTPException(404, f"{filename} not available (generation may have failed)")
    media = {
        ".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".md": "text/markdown; charset=utf-8",
        ".zip": "application/zip",
    }.get(path.suffix.lower(), "application/octet-stream")
    return FileResponse(path=str(path), media_type=media, filename=path.name)


@router.get("/jobs/{job_id}/export/file/{filename}")
def export_job_file(job_id: int, filename: str, db: Session = Depends(get_db)):
    from fastapi.responses import FileResponse

    from app.services.document_export import is_standard_packet_filename
    from app.services.packet_store import export_bundle_files

    if not is_standard_packet_filename(filename):
        raise HTTPException(400, "Invalid export filename")
    gen = generate_packet(job_id, db)
    job = db.get(Job, job_id)
    company = job.company if job else "company"
    title = job.title if job else "role"
    bundle = export_bundle_files(
        resume=gen.tailored_resume,
        cover=gen.cover_letter,
        portfolio_url=PORTFOLIO_URL,
        company=company,
        title=title,
        job_id=job_id,
    )
    path = Path(bundle["folder"]) / filename
    if not path.exists():
        raise HTTPException(404, f"{filename} not available")
    media = {
        ".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".md": "text/markdown; charset=utf-8",
    }.get(path.suffix.lower(), "application/octet-stream")
    return FileResponse(path=str(path), media_type=media, filename=path.name)


@router.get("/analytics")
def recruiter_analytics(db: Session = Depends(get_db)):
    from app.services.recruiter_analytics import build_analytics_dashboard

    return build_analytics_dashboard(db)


@router.get("/analytics/followups")
def analytics_followups(db: Session = Depends(get_db)):
    from app.services.recruiter_analytics import build_followups, load_applications

    return {
        "auto_send": False,
        "approval_required": True,
        "followups": build_followups(load_applications(db)),
    }


@router.post("/analytics/followups/{app_id}/approve")
def approve_followup_email(
    app_id: int,
    cadence_days: int = Query(3, ge=3, le=14),
    db: Session = Depends(get_db),
):
    from app.services.recruiter_analytics import approve_followup

    if cadence_days not in {3, 7, 14}:
        raise HTTPException(400, "cadence_days must be 3, 7, or 14")
    try:
        return approve_followup(db, app_id, cadence_days)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.get("/analytics/export/{fmt}")
def analytics_export(fmt: str, db: Session = Depends(get_db)):
    from fastapi.responses import Response

    from app.services.recruiter_analytics import (
        export_csv,
        export_excel_bytes,
        export_json,
        export_pdf_bytes,
        load_applications,
    )

    fmt = (fmt or "").lower().strip()
    apps = load_applications(db)
    if fmt == "csv":
        return Response(
            content=export_csv(apps),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=recruiter_analytics.csv"},
        )
    if fmt == "json":
        return Response(
            content=export_json(db),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=recruiter_analytics.json"},
        )
    if fmt in {"xlsx", "excel"}:
        return Response(
            content=export_excel_bytes(apps),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=recruiter_analytics.xlsx"},
        )
    if fmt == "pdf":
        return Response(
            content=export_pdf_bytes(db),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=recruiter_analytics.pdf"},
        )
    raise HTTPException(400, "Supported formats: csv, excel, xlsx, pdf, json")


# --- Application Assistant (local hiring process) ---


@router.get("/assistant")
def assistant_home(db: Session = Depends(get_db)):
    from app.services.application_assistant import assistant_overview

    return assistant_overview(db)


@router.post("/assistant/prepare/{job_id}")
def assistant_prepare(job_id: int, db: Session = Depends(get_db)):
    from app.services.application_assistant import prepare_application

    try:
        return prepare_application(job_id, db)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.get("/assistant/applications/{app_id}")
def assistant_get_application(app_id: int, db: Session = Depends(get_db)):
    from app.services.application_assistant import assistant_bundle

    row = db.get(Application, app_id)
    if not row:
        raise HTTPException(404, "Application not found")
    return assistant_bundle(row)


@router.patch("/assistant/applications/{app_id}/checklist")
def assistant_checklist(app_id: int, payload: dict, db: Session = Depends(get_db)):
    from app.services.application_assistant import update_checklist

    try:
        return update_checklist(app_id, payload or {}, db)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.patch("/assistant/applications/{app_id}/notes")
def assistant_notes(app_id: int, payload: dict, db: Session = Depends(get_db)):
    from app.services.application_assistant import update_notes

    try:
        return update_notes(app_id, payload or {}, db)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.get("/assistant/calendar")
def assistant_calendar(db: Session = Depends(get_db)):
    from app.services.application_assistant import list_calendar

    return {"events": list_calendar(db), "fabricated": False, "local_only": True}


@router.post("/assistant/applications/{app_id}/calendar")
def assistant_calendar_upsert(app_id: int, payload: dict, db: Session = Depends(get_db)):
    from app.services.application_assistant import upsert_calendar_event

    try:
        return upsert_calendar_event(app_id, payload or {}, db)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.delete("/assistant/applications/{app_id}/calendar/{event_id}")
def assistant_calendar_delete(app_id: int, event_id: str, db: Session = Depends(get_db)):
    from app.services.application_assistant import delete_calendar_event

    try:
        return delete_calendar_event(app_id, event_id, db)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.get("/assistant/lessons")
def assistant_lessons(db: Session = Depends(get_db)):
    from app.services.application_assistant import list_lessons

    return {"lessons": list_lessons(db), "fabricated": False, "local_only": True}


@router.post("/assistant/applications/{app_id}/lessons")
def assistant_add_lesson(app_id: int, payload: dict, db: Session = Depends(get_db)):
    from app.services.application_assistant import add_lesson

    try:
        return add_lesson(app_id, payload or {}, db)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.get("/assistant/offers")
def assistant_offers(db: Session = Depends(get_db)):
    from app.services.application_assistant import compare_offers

    return compare_offers(db)


@router.patch("/assistant/applications/{app_id}/offer")
def assistant_offer(app_id: int, payload: dict, db: Session = Depends(get_db)):
    from app.services.application_assistant import update_offer

    try:
        return update_offer(app_id, payload or {}, db)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


# --- Safe Application Autofill (localhost companion) ---


@router.get("/autofill/health")
def autofill_health():
    return {
        "status": "ok",
        "mode": "safe_autofill",
        "auto_submit": False,
        "captcha_bypass": False,
        "local_only": True,
        "api_base": "http://127.0.0.1:8787",
    }


@router.get("/autofill/active")
def autofill_active():
    from app.services.safe_autofill import get_active_session

    session = get_active_session()
    if not session:
        return {"active": False, "session": None, "auto_submit": False}
    return {"active": True, "session": session, "auto_submit": False}


@router.post("/autofill/applications/{app_id}/open")
def autofill_open(app_id: int, db: Session = Depends(get_db)):
    """Opens Review-and-Submit session (confirm required; never auto-submits)."""
    from app.services.review_submit import open_review_session

    try:
        payload = open_review_session(app_id, db)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    return payload


@router.get("/autofill/applications/{app_id}/payload")
def autofill_payload(app_id: int, db: Session = Depends(get_db)):
    from app.services.safe_autofill import build_autofill_payload

    row = db.get(Application, app_id)
    if not row:
        raise HTTPException(404, "Application not found")
    return build_autofill_payload(row, db)


@router.post("/autofill/applications/{app_id}/classify")
def autofill_classify(app_id: int, payload: dict, db: Session = Depends(get_db)):
    from app.services.safe_autofill import build_autofill_payload, classify_detected_fields

    row = db.get(Application, app_id)
    if not row:
        raise HTTPException(404, "Application not found")
    session = build_autofill_payload(row, db)
    detected = (payload or {}).get("detected") or []
    classification = classify_detected_fields(detected)
    return {
        "application_id": app_id,
        "company": session["company"],
        "position": session["position"],
        "platform": session["platform"],
        "files": session["files"],
        "safety_check": session["safety_check"],
        "classification": classification,
        "requires_confirm_autofill": True,
        "never_click_submit": True,
        "auto_submit": False,
    }


@router.post("/autofill/applications/{app_id}/suggest-answer")
def autofill_suggest(app_id: int, payload: dict, db: Session = Depends(get_db)):
    from app.services.safe_autofill import suggest_answer

    try:
        return suggest_answer(app_id, (payload or {}).get("question") or "", db)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.post("/autofill/applications/{app_id}/mark-submitted")
def autofill_mark_submitted(app_id: int, payload: dict | None = None, db: Session = Depends(get_db)):
    from app.services.safe_autofill import mark_submitted

    body = payload or {}
    try:
        return mark_submitted(
            app_id,
            db,
            application_url=body.get("application_url"),
            platform=body.get("platform"),
            notes=body.get("notes"),
            resume_version=body.get("resume_version"),
            cover_version=body.get("cover_version"),
            confirmation_number=body.get("confirmation_number"),
            match_score=body.get("match_score"),
            marked_via=body.get("marked_via") or "safe_autofill",
        )
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.post("/applications/{app_id}/mark-submitted")
def mark_application_submitted(app_id: int, payload: dict | None = None, db: Session = Depends(get_db)):
    """Alias used by Job Machine UI after manual submit."""
    return autofill_mark_submitted(app_id, payload, db)


# --- Review-and-Submit Assistant (never auto-submits) ---


@router.get("/review-submit/applications/{app_id}/panel")
def review_submit_panel(app_id: int, db: Session = Depends(get_db)):
    from app.services.review_submit import get_review_panel

    try:
        return get_review_panel(app_id, db)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.post("/review-submit/applications/{app_id}/open")
def review_submit_open(app_id: int, db: Session = Depends(get_db)):
    from app.services.review_submit import open_review_session

    try:
        return open_review_session(app_id, db)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.post("/review-submit/applications/{app_id}/autofill-confirmed")
def review_submit_autofill_confirmed(app_id: int, payload: dict | None = None, db: Session = Depends(get_db)):
    from app.services.review_submit import record_autofill_confirmed

    try:
        return record_autofill_confirmed(app_id, db, payload or {})
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.post("/review-submit/applications/{app_id}/ready-for-final-review")
def review_submit_ready(app_id: int, payload: dict | None = None, db: Session = Depends(get_db)):
    from app.services.review_submit import ready_for_final_review

    try:
        return ready_for_final_review(app_id, db, payload or {})
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.post("/review-submit/applications/{app_id}/confirm-submission")
def review_submit_confirm(app_id: int, payload: dict | None = None, db: Session = Depends(get_db)):
    from app.services.review_submit import confirm_submission

    body = payload or {}
    try:
        return confirm_submission(
            app_id,
            db,
            outcome=body.get("outcome") or "",
            confirmation_number=body.get("confirmation_number"),
            notes=body.get("notes"),
            application_url=body.get("application_url"),
            platform=body.get("platform"),
        )
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.get("/review-submit/applications/{app_id}/duplicate-check")
def review_submit_duplicate(app_id: int, db: Session = Depends(get_db)):
    from app.services.review_submit import check_duplicate_application

    try:
        return check_duplicate_application(db, app_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.get("/autofill/applications/{app_id}/files/{kind}")
def autofill_download_file(
    app_id: int,
    kind: str,
    format: str | None = Query(None, description="pdf|docx|md — default prefers pdf then docx"),
    db: Session = Depends(get_db),
):
    from fastapi.responses import FileResponse

    from app.services.safe_autofill import ensure_application_files, verify_file_belongs_to_application

    row = db.get(Application, app_id)
    if not row:
        raise HTTPException(404, "Application not found")
    job = db.get(Job, row.job_id) if row.job_id else None
    files = ensure_application_files(row, job)
    kind = (kind or "").lower()
    fmt = (format or "").lower().strip() or None
    if kind not in {"resume", "cover"}:
        raise HTTPException(400, "kind must be resume or cover")

    candidates: list[tuple[str | None, str]] = []
    if kind == "resume":
        if fmt == "pdf":
            candidates = [(files.get("resume_pdf"), "application/pdf")]
        elif fmt == "docx":
            candidates = [
                (
                    files.get("resume_docx"),
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            ]
        elif fmt == "md":
            candidates = [(files.get("resume_md"), "text/markdown; charset=utf-8")]
        else:
            # Prefer PDF, fall back to DOCX, then md/txt
            candidates = [
                (files.get("resume_pdf"), "application/pdf"),
                (
                    files.get("resume_docx"),
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ),
                (files.get("resume_md"), "text/markdown; charset=utf-8"),
                (files.get("resume_txt"), "text/plain"),
            ]
    else:
        if fmt == "pdf":
            candidates = [(files.get("cover_pdf"), "application/pdf")]
        elif fmt == "docx":
            candidates = [
                (
                    files.get("cover_docx"),
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            ]
        elif fmt == "md":
            candidates = [(files.get("cover_md"), "text/markdown; charset=utf-8")]
        else:
            candidates = [
                (files.get("cover_pdf"), "application/pdf"),
                (
                    files.get("cover_docx"),
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ),
                (files.get("cover_md"), "text/markdown; charset=utf-8"),
                (files.get("cover_txt"), "text/plain"),
            ]

    path = None
    media = "application/octet-stream"
    for candidate, mime in candidates:
        if candidate and Path(candidate).exists():
            path = candidate
            media = mime
            break
    if not path:
        raise HTTPException(404, "File not prepared. Run Prepare Application / Export Packet first.")

    p = Path(path)
    if not verify_file_belongs_to_application(app_id, p.name, db):
        raise HTTPException(400, "File failed company/role verification — refusing download.")
    return FileResponse(path=str(p), media_type=media, filename=p.name)


@router.post("/autofill/log")
def autofill_client_log(payload: dict):
    from app.services.safe_autofill import _append_log

    _append_log("extension", payload or {})
    return {"ok": True, "telemetry": False}
