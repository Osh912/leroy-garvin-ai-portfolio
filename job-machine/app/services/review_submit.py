from __future__ import annotations

"""
Review-and-Submit Assistant — fastest safe apply workflow.
Never auto-submits. Never clicks Submit. Never bypasses CAPTCHA.
"""

from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from app.models import Application, Job
from app.services.safe_autofill import (
    _append_log,
    _meta,
    _save_meta,
    build_autofill_payload,
    detect_platform,
    ensure_application_files,
    get_active_session,
    mark_submitted,
    open_application_session,
    set_active_session,
    verified_autofill_fields,
)

WORKFLOW_STEPS = [
    "Job Card",
    "Prepare Application",
    "Review Resume and Cover Letter",
    "Approve to Apply",
    "Open Official Application",
    "Preview Autofill",
    "Confirm Autofill",
    "Manual Review",
    "Leroy Clicks Submit",
    "Confirm Submission",
    "Mark Applied",
]

SUBMISSION_CHECKLIST_KEYS = [
    ("correct_company", "Correct company"),
    ("correct_job_title", "Correct job title"),
    ("official_application_url", "Official application URL"),
    ("fully_remote_verified", "Fully remote status verified"),
    ("correct_resume_attached", "Correct resume attached"),
    ("correct_cover_letter_attached", "Correct cover letter attached"),
    ("portfolio_url_included", "Portfolio URL included"),
    ("linkedin_url_included", "LinkedIn URL included"),
    ("contact_information_correct", "Contact information correct"),
    ("employment_history_correct", "Employment history correct"),
    ("required_questions_completed", "Required questions completed"),
    ("sensitive_questions_reviewed_manually", "Sensitive questions reviewed manually"),
    ("no_unsupported_claims_detected", "No unsupported claims detected"),
    ("no_blank_required_fields", "No blank required fields"),
]


def workflow_state(row: Application) -> dict[str, Any]:
    meta = _meta(row)
    rs = meta.get("review_submit") or {}
    completed = set(rs.get("completed_steps") or [])
    if row.tailored_resume and row.cover_letter:
        completed.add("Prepare Application")
        completed.add("Review Resume and Cover Letter")
    if row.status in {"approved_to_apply", "in_progress", "needs_verification", "applied"} or rs.get(
        "approved_to_apply_at"
    ):
        completed.add("Approve to Apply")
    if (meta.get("autofill") or {}).get("last_opened_at"):
        completed.add("Open Official Application")
        completed.add("Preview Autofill")
    if rs.get("autofill_confirmed_at"):
        completed.add("Confirm Autofill")
        completed.add("Manual Review")
    if rs.get("ready_for_final_review_at"):
        completed.add("Manual Review")
    if row.status == "applied" or (meta.get("submission") or {}).get("submitted_at"):
        completed.update(
            [
                "Leroy Clicks Submit",
                "Confirm Submission",
                "Mark Applied",
            ]
        )
    steps = [
        {"name": name, "done": name in completed, "index": i + 1}
        for i, name in enumerate(WORKFLOW_STEPS)
    ]
    next_step = next((s["name"] for s in steps if not s["done"]), "Complete")
    return {
        "steps": steps,
        "completed_steps": sorted(completed),
        "next_step": next_step,
        "auto_submit": False,
        "never_click_submit": True,
    }


def build_submission_checklist(row: Application, job: Job | None, files: dict[str, Any]) -> dict[str, Any]:
    fields = verified_autofill_fields()
    meta = _meta(row)
    rs = meta.get("review_submit") or {}
    url = (job.url if job else "") or ""
    remote_ok = False
    if job:
        blob = f"{job.location or ''} {job.description or ''}".lower()
        remote_ok = "remote" in blob and "hybrid" not in blob
    else:
        remote_ok = "remote" in (row.location or "").lower()

    items = {
        "correct_company": bool(row.company) and (not job or row.company == job.company),
        "correct_job_title": bool(row.position) and (not job or row.position == job.title),
        "official_application_url": bool(url),
        "fully_remote_verified": remote_ok,
        "correct_resume_attached": bool(row.tailored_resume and files.get("resume_txt")),
        "correct_cover_letter_attached": bool(row.cover_letter and files.get("cover_txt")),
        "portfolio_url_included": bool(fields.get("portfolio")),
        "linkedin_url_included": bool(fields.get("linkedin")),
        "contact_information_correct": bool(fields.get("email") and fields.get("phone")),
        "employment_history_correct": bool(fields.get("employment_history") or row.tailored_resume),
        "required_questions_completed": bool(rs.get("required_questions_acked")),
        "sensitive_questions_reviewed_manually": bool(rs.get("sensitive_acked")),
        "no_unsupported_claims_detected": not bool((meta.get("truth_warnings") or [])),
        "no_blank_required_fields": bool(rs.get("no_blank_required_acked")),
    }
    labeled = [
        {"key": k, "label": label, "ok": bool(items[k]), "leroy_confirm_required": k.endswith("_acked") or k in {
            "required_questions_completed",
            "sensitive_questions_reviewed_manually",
            "no_blank_required_fields",
            "fully_remote_verified",
        }}
        for k, label in SUBMISSION_CHECKLIST_KEYS
    ]
    return {
        "items": items,
        "labeled": labeled,
        "all_system_checks_pass": all(
            items[k]
            for k in items
            if k
            not in {
                "required_questions_completed",
                "sensitive_questions_reviewed_manually",
                "no_blank_required_fields",
                "fully_remote_verified",
            }
        ),
        "ready_for_final_review_enabled": True,
        "ready_for_final_review_submits": False,
        "button_label": "READY FOR FINAL REVIEW",
        "note": "READY FOR FINAL REVIEW never submits the application. Leroy must click the employer Submit button.",
    }


def check_duplicate_application(db: Session, app_id: int) -> dict[str, Any]:
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    twins = (
        db.query(Application)
        .filter(
            Application.id != app_id,
            Application.company == row.company,
            Application.position == row.position,
            Application.status.in_(["applied", "needs_verification"]),
        )
        .all()
    )
    return {
        "duplicate_warning": len(twins) > 0,
        "prior_applications": [
            {
                "id": t.id,
                "status": t.status,
                "date_applied": t.date_applied.isoformat() if t.date_applied else None,
            }
            for t in twins
        ],
        "message": (
            f"Warning: you already marked Applied for {row.company} — {row.position}."
            if twins
            else None
        ),
    }


def open_review_session(app_id: int, db: Session) -> dict[str, Any]:
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    if row.status not in {
        "approved_to_apply",
        "in_progress",
        "needs_verification",
        "ready",
        "saved",
        "applied",
    }:
        pass
    dup = check_duplicate_application(db, app_id)
    payload = open_application_session(app_id, db)
    job = db.get(Job, row.job_id) if row.job_id else None
    files = payload.get("files") or {}
    checklist = build_submission_checklist(row, job, files)
    wf = workflow_state(row)
    meta = _meta(row)
    rs = meta.setdefault("review_submit", {})
    rs["last_opened_at"] = datetime.utcnow().isoformat() + "Z"
    if row.status in {"ready", "saved"}:
        # Soft note — prefer Approve first, but do not hard-block Open if materials exist
        rs["opened_before_approve"] = True
    _save_meta(row, meta)
    if row.status == "approved_to_apply":
        row.status = "in_progress"
    db.add(row)
    db.commit()

    enriched = {
        **payload,
        "mode": "review_and_submit",
        "workflow": wf,
        "submission_checklist": checklist,
        "duplicate_check": dup,
        "file_filenames": {
            "resume": (files.get("resume_pdf") or files.get("resume_txt") or files.get("resume_md") or "").split("/")[
                -1
            ],
            "cover": (files.get("cover_pdf") or files.get("cover_txt") or files.get("cover_md") or "").split("/")[-1],
        },
        "error_hints": {
            "expired_listing": "If the page says the job is closed/expired, stop and mark Needs Verification.",
            "sign_in": "Complete employer sign-in yourself. Job Machine never stores passwords or tokens.",
            "captcha": "Solve CAPTCHA yourself. Never bypass platform protections.",
            "unsupported_ats": "Use Manual Review for unsupported forms. LinkedIn Easy Apply stays manual.",
            "upload_failure": "Download the labeled files and attach them manually in highlighted file inputs.",
            "wrong_packet": "Attachment is blocked when company/role tokens do not match.",
        },
        "platforms_supported": [
            "greenhouse",
            "lever",
            "ashby",
            "smartrecruiters",
            "workday",
            "workable",
            "generic",
        ],
        "platforms_manual_only": ["linkedin", "indeed"],
        "panel": {
            "title": "Review & Submit Assistant",
            "ready_button": "READY FOR FINAL REVIEW",
            "ready_button_submits": False,
            "confirm_prompt": "DID THE APPLICATION SUBMIT SUCCESSFULLY?",
            "confirm_options": [
                {"id": "yes", "label": "Yes — Mark Applied"},
                {"id": "no", "label": "No — Keep In Progress"},
                {"id": "unsure", "label": "Unsure — Needs Verification"},
            ],
        },
    }
    set_active_session(enriched)
    _append_log(
        "job_opened",
        {
            "application_id": app_id,
            "platform": enriched.get("platform"),
            "company": row.company,
            "duplicate_warning": dup.get("duplicate_warning"),
        },
    )
    return enriched


def record_autofill_confirmed(app_id: int, db: Session, details: dict[str, Any] | None = None) -> dict[str, Any]:
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    meta = _meta(row)
    rs = meta.setdefault("review_submit", {})
    rs["autofill_confirmed_at"] = datetime.utcnow().isoformat() + "Z"
    rs["autofill_details"] = {
        "fields_autofilled": (details or {}).get("filled") or [],
        "fields_skipped": (details or {}).get("skipped") or [],
        # Never persist sensitive answer values
    }
    _save_meta(row, meta)
    db.add(row)
    db.commit()
    session = get_active_session() or {}
    if session.get("application_id") == app_id:
        session["status"] = "awaiting_manual_review"
        session["autofill_confirmed"] = True
        set_active_session(session)
    _append_log(
        "fields_autofilled",
        {
            "application_id": app_id,
            "filled_count": len(rs["autofill_details"]["fields_autofilled"]),
            "skipped_count": len(rs["autofill_details"]["fields_skipped"]),
        },
    )
    return {"ok": True, "status": "awaiting_manual_review", "auto_submit": False}


def ready_for_final_review(app_id: int, db: Session, acks: dict[str, Any] | None = None) -> dict[str, Any]:
    """Mark checklist acknowledgements. NEVER submits the employer application."""
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    job = db.get(Job, row.job_id) if row.job_id else None
    files = ensure_application_files(row, job)
    meta = _meta(row)
    rs = meta.setdefault("review_submit", {})
    body = acks or {}
    if body.get("required_questions_completed"):
        rs["required_questions_acked"] = True
    if body.get("sensitive_questions_reviewed_manually"):
        rs["sensitive_acked"] = True
    if body.get("no_blank_required_fields"):
        rs["no_blank_required_acked"] = True
    if body.get("fully_remote_verified"):
        rs["remote_acked"] = True
    rs["ready_for_final_review_at"] = datetime.utcnow().isoformat() + "Z"
    _save_meta(row, meta)
    db.add(row)
    db.commit()
    checklist = build_submission_checklist(row, job, files)
    session = get_active_session() or {}
    if session.get("application_id") == app_id:
        session["status"] = "awaiting_leroy_submit"
        session["submission_checklist"] = checklist
        session["ready_for_final_review"] = True
        set_active_session(session)
    _append_log(
        "manual_review_items",
        {
            "application_id": app_id,
            "ready_for_final_review": True,
            "submits": False,
            "checklist": checklist["items"],
        },
    )
    return {
        "application_id": app_id,
        "ready_for_final_review": True,
        "submits_application": False,
        "auto_submit": False,
        "never_click_submit": True,
        "message": "READY FOR FINAL REVIEW — Leroy must click the employer's Submit button. Job Machine will not submit.",
        "submission_checklist": checklist,
        "workflow": workflow_state(row),
        "next": "Leroy Clicks Submit",
    }


def confirm_submission(
    app_id: int,
    db: Session,
    *,
    outcome: str,
    confirmation_number: str | None = None,
    notes: str | None = None,
    application_url: str | None = None,
    platform: str | None = None,
) -> dict[str, Any]:
    """
    After Leroy personally submits (or attempts):
    - yes → Mark Applied + follow-up dates
    - no → Keep In Progress
    - unsure → Needs Verification
    """
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    outcome = (outcome or "").strip().lower()
    if outcome not in {"yes", "no", "unsure"}:
        raise ValueError("outcome must be yes, no, or unsure")

    job = db.get(Job, row.job_id) if row.job_id else None
    url = application_url or (job.url if job else "") or ""
    plat = platform or detect_platform(url)
    meta = _meta(row)
    rs = meta.setdefault("review_submit", {})
    now = datetime.utcnow()
    rs["submission_outcome"] = outcome
    rs["submission_outcome_at"] = now.isoformat() + "Z"

    if outcome == "no":
        row.status = "in_progress"
        _save_meta(row, meta)
        db.add(row)
        db.commit()
        _append_log("submission_confirmation", {"application_id": app_id, "outcome": "no"})
        return {
            "application_id": app_id,
            "status": "in_progress",
            "outcome": "no",
            "auto_submit": False,
            "message": "Kept In Progress. Fix blockers, then try again — Submit is still never clicked for you.",
        }

    if outcome == "unsure":
        row.status = "needs_verification"
        stamp = f"\n[{now.isoformat()}Z] Submission unsure — Needs Verification."
        row.notes = ((row.notes or "").rstrip() + stamp).strip()
        _save_meta(row, meta)
        db.add(row)
        db.commit()
        _append_log("submission_confirmation", {"application_id": app_id, "outcome": "unsure"})
        return {
            "application_id": app_id,
            "status": "needs_verification",
            "outcome": "unsure",
            "auto_submit": False,
            "message": "Marked Needs Verification. Confirm on the employer site, then Yes — Mark Applied when sure.",
        }

    # yes → Mark Applied via existing safe path + richer metadata
    followups = {
        "check_3_day": (date.today() + timedelta(days=3)).isoformat(),
        "followup_7_day": (date.today() + timedelta(days=7)).isoformat(),
        "final_followup_14_day": (date.today() + timedelta(days=14)).isoformat(),
        "auto_send": False,
        "note": "Suggested dates only — do not send messages automatically.",
    }
    result = mark_submitted(
        app_id,
        db,
        application_url=url,
        platform=plat,
        notes=notes or "Manually submitted by Leroy. Review-and-Submit Assistant did not click Submit.",
        resume_version=None,
        cover_version=None,
        confirmation_number=confirmation_number,
        follow_up_dates=followups,
        match_score=float(row.application_score or 0) or None,
        marked_via="review_and_submit",
    )
    db.refresh(row)
    meta = _meta(row)
    meta.setdefault("review_submit", {})["marked_applied_at"] = now.isoformat() + "Z"
    _save_meta(row, meta)
    db.add(row)
    db.commit()
    _append_log(
        "tracker_update",
        {
            "application_id": app_id,
            "status": "applied",
            "outcome": "yes",
            "platform": plat,
            "confirmation_number_present": bool(confirmation_number),
        },
    )
    return {
        **result,
        "outcome": "yes",
        "follow_up_dates": followups,
        "message": "Marked Applied. Follow-up dates suggested (3/7/14). Nothing was emailed automatically.",
    }


def get_review_panel(app_id: int, db: Session) -> dict[str, Any]:
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    job = db.get(Job, row.job_id) if row.job_id else None
    payload = build_autofill_payload(row, db)
    files = payload.get("files") or {}
    return {
        "application_id": app_id,
        "company": row.company,
        "position": row.position,
        "status": row.status,
        "workflow": workflow_state(row),
        "submission_checklist": build_submission_checklist(row, job, files),
        "duplicate_check": check_duplicate_application(db, app_id),
        "files": files,
        "file_filenames": {
            "resume": (files.get("resume_pdf") or files.get("resume_txt") or files.get("resume_md") or "").split("/")[
                -1
            ],
            "cover": (files.get("cover_pdf") or files.get("cover_txt") or files.get("cover_md") or "").split("/")[-1],
        },
        "platform": payload.get("platform"),
        "application_url": payload.get("application_url"),
        "auto_submit": False,
        "never_click_submit": True,
        "match_score": row.application_score,
    }
