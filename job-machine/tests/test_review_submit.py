from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Application, Job
from app.services.interview_pipeline import approve_application
from app.services.review_submit import (
    WORKFLOW_STEPS,
    check_duplicate_application,
    confirm_submission,
    open_review_session,
    ready_for_final_review,
    record_autofill_confirmed,
)
from app.services.safe_autofill import detect_platform, is_sensitive_question, suggest_answer


def _session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


_app_seq = 0


def _app(db, *, company="GitLab", title="Technical Support Engineer", status="ready"):
    global _app_seq
    _app_seq += 1
    job = Job(
        external_id=f"rs-{_app_seq}-{company}-{title}",
        source="greenhouse",
        company=company,
        title=title,
        location="Remote — United States",
        url="https://boards.greenhouse.io/gitlab/jobs/999",
        description="Fully remote technical support role",
        salary_text="$90,000",
    )
    db.add(job)
    db.commit()
    app = Application(
        job_id=job.id,
        company=company,
        position=title,
        salary="$90,000",
        location="Remote",
        status=status,
        tailored_resume=f"Leroy Garvin Jr\n{company}\n{title}\n",
        cover_letter=f"Dear {company} team,\nI am interested in {title}.\n",
        portfolio_refs='[{"name":"LawOne AI","url":"https://leroy-garvin-ai-portfolio.vercel.app"}]',
        application_score=82,
        analytics_json='{"resume_version":"B","cover_version":"A"}',
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


def test_workflow_steps_exact_order():
    assert WORKFLOW_STEPS[0] == "Job Card"
    assert WORKFLOW_STEPS[-1] == "Mark Applied"
    assert "Approve to Apply" in WORKFLOW_STEPS
    assert WORKFLOW_STEPS.index("Approve to Apply") < WORKFLOW_STEPS.index("Open Official Application")
    assert WORKFLOW_STEPS.index("Confirm Autofill") < WORKFLOW_STEPS.index("Leroy Clicks Submit")
    assert WORKFLOW_STEPS.index("Confirm Submission") < WORKFLOW_STEPS.index("Mark Applied")


def test_approve_does_not_mark_applied():
    db = _session()
    app = _app(db)
    row = approve_application(db, app.id)
    assert row.status == "approved_to_apply"
    assert row.date_applied is None


def test_open_session_checklist_and_never_autosubmit():
    db = _session()
    app = _app(db)
    approve_application(db, app.id)
    payload = open_review_session(app.id, db)
    assert payload["auto_submit"] is False
    assert payload["never_click_submit"] is True
    assert payload["requires_confirm_autofill"] is True
    assert payload["mode"] == "review_and_submit"
    assert payload["submission_checklist"]["ready_for_final_review_submits"] is False
    assert payload["submission_checklist"]["button_label"] == "READY FOR FINAL REVIEW"
    assert payload["file_filenames"]["resume"] in {"resume.pdf", "resume.docx", "resume.md"}
    assert "resume" in payload["file_filenames"]["resume"]
    assert "workable" in payload["platforms_supported"]
    db.refresh(app)
    assert app.status == "in_progress"


def test_ready_for_final_review_never_submits():
    db = _session()
    app = _app(db)
    result = ready_for_final_review(
        app.id,
        db,
        {
            "required_questions_completed": True,
            "sensitive_questions_reviewed_manually": True,
            "no_blank_required_fields": True,
        },
    )
    assert result["submits_application"] is False
    assert result["auto_submit"] is False
    assert result["never_click_submit"] is True
    db.refresh(app)
    assert app.status != "applied"


def test_confirm_yes_marks_applied_with_followups():
    db = _session()
    app = _app(db)
    record_autofill_confirmed(app.id, db, {"filled": [{"key": "email"}], "skipped": []})
    ready_for_final_review(app.id, db, {"sensitive_questions_reviewed_manually": True})
    result = confirm_submission(
        app.id,
        db,
        outcome="yes",
        confirmation_number="GH-123",
        notes="Submitted myself",
    )
    assert result["outcome"] == "yes"
    assert result["auto_submit"] is False
    assert result["status"] == "applied"
    assert result["follow_up_dates"]["check_3_day"]
    assert result["follow_up_dates"]["followup_7_day"]
    assert result["follow_up_dates"]["final_followup_14_day"]
    assert result["follow_up_dates"]["auto_send"] is False
    assert result["submission"]["confirmation_number"] == "GH-123"
    db.refresh(app)
    assert app.status == "applied"
    assert app.date_applied is not None


def test_confirm_no_and_unsure():
    db = _session()
    app = _app(db)
    no = confirm_submission(app.id, db, outcome="no")
    assert no["status"] == "in_progress"
    db.refresh(app)
    assert app.status == "in_progress"
    unsure = confirm_submission(app.id, db, outcome="unsure")
    assert unsure["status"] == "needs_verification"
    db.refresh(app)
    assert app.status == "needs_verification"


def test_duplicate_warning():
    db = _session()
    a1 = _app(db)
    confirm_submission(a1.id, db, outcome="yes")
    a2 = _app(db, company="GitLab", title="Technical Support Engineer")
    dup = check_duplicate_application(db, a2.id)
    assert dup["duplicate_warning"] is True


def test_sensitive_and_start_date_manual():
    assert is_sensitive_question("Willingness to relocate")
    assert is_sensitive_question("When can you start?")
    assert is_sensitive_question("I agree to the terms and conditions")
    assert is_sensitive_question("Highest degree earned")
    db = _session()
    app = _app(db)
    sens = suggest_answer(app.id, "Desired compensation?", db)
    assert sens["label"] == "MANUAL REVIEW REQUIRED"
    assert sens["suggested_answer"] is None
    draft = suggest_answer(app.id, "What tools have you used?", db)
    assert draft["suggested_answer"]
    assert draft["label"] == "Suggested Answer"
    assert draft["auto_fill"] is False


def test_workable_platform_and_fixture():
    assert detect_platform("https://apply.workable.com/acme/j/ABC") == "workable"
    fixture = Path(__file__).resolve().parents[2] / "browser-extension" / "fixtures" / "workable.html"
    assert fixture.exists()
    text = fixture.read_text(encoding="utf-8")
    assert "data-jm-fixture-platform=\"workable\"" in text
    assert "Submit Application" in text


def test_extension_never_clicks_submit_and_has_review_panel():
    root = Path(__file__).resolve().parents[2] / "browser-extension"
    content = (root / "content" / "content.js").read_text(encoding="utf-8")
    safety = (root / "lib" / "safety.js").read_text(encoding="utf-8")
    assert "Confirm Autofill" in content
    assert "READY FOR FINAL REVIEW" in content
    assert "Yes — Mark Applied" in content
    assert "Submit was NOT clicked" in content or "Submit will NOT" in content
    assert "neverClickSubmit" in safety
    assert "return false" in safety
    # Ensure no programmatic click of submit
    assert ".click()" not in content or "neverClickSubmit" in content
