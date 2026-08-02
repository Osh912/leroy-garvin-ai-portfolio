from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Application, Job
from app.services.application_assistant import (
    add_lesson,
    assistant_overview,
    compare_offers,
    compute_checklist_from_materials,
    list_calendar,
    prepare_application,
    update_notes,
    update_offer,
    upsert_calendar_event,
)


def _session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def _job(db, **kwargs):
    job = Job(
        external_id=kwargs.get("external_id", "asst-1"),
        source="test",
        company=kwargs.get("company", "GitLab"),
        title=kwargs.get("title", "Technical Support Engineer"),
        location="Remote - United States",
        url="https://example.com/jobs/asst-1",
        description=kwargs.get(
            "description",
            "Fully remote technical support. Build n8n workflows and help customers. Entry level welcome.",
        ),
        salary_text="$80,000 – $95,000",
        salary_min=80000,
        salary_max=95000,
        tags="support,automation",
        is_remote=1,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def test_checklist_never_invents_completion():
    cl = compute_checklist_from_materials(resume="", cover="")
    assert cl["resume_attached"] is False
    assert cl["cover_letter_attached"] is False
    assert cl["job_requirements_reviewed"] is False


def test_checklist_detects_real_materials():
    resume = """Leroy Garvin Jr
AlignedVibesCo@gmail.com
(912) 901-6378
https://leroy-garvin-ai-portfolio.vercel.app
https://www.linkedin.com/in/leroy-garvin-49443b423/
"""
    cover = "Please see my portfolio https://leroy-garvin-ai-portfolio.vercel.app"
    cl = compute_checklist_from_materials(resume=resume, cover=cover)
    assert cl["resume_attached"] is True
    assert cl["cover_letter_attached"] is True
    assert cl["portfolio_url_included"] is True
    assert cl["linkedin_included"] is True
    assert cl["contact_information_verified"] is True
    assert cl["job_requirements_reviewed"] is False


def test_prepare_application_local_bundle():
    db = _session()
    job = _job(db)
    bundle = prepare_application(job.id, db)
    assert bundle["fabricated"] is False
    assert bundle["auto_apply"] is False
    assert bundle["local_only"] is True
    assert bundle["tailored_resume"]
    assert bundle["cover_letter"]
    assert bundle["recruiter_summary"]
    assert "GitLab" in bundle["recruiter_summary"]
    assert bundle["checklist"]["resume_attached"] is True
    assert bundle["checklist"]["job_requirements_reviewed"] is False
    assert db.query(Application).count() == 1


def test_notes_calendar_lessons_offers_from_real_input_only():
    db = _session()
    job = _job(db)
    bundle = prepare_application(job.id, db)
    app_id = bundle["application_id"]

    notes = update_notes(
        app_id,
        {
            "recruiter_name": "Alex Recruiter",
            "hiring_manager": "Sam Manager",
            "referral": "None",
            "interview_notes": "Asked about n8n",
            "salary_discussed": "$90k mentioned by recruiter",
            "follow_up_reminders": "Send thank-you tomorrow",
        },
        db,
    )
    assert notes["application_notes"]["recruiter_name"] == "Alex Recruiter"

    cal = upsert_calendar_event(
        app_id,
        {
            "date": "2026-08-15",
            "time": "14:00",
            "company": "GitLab",
            "interview_stage": "phone_screen",
            "meeting_link": "https://meet.example.com/abc",
            "interviewers": "Alex Recruiter, Sam Manager",
        },
        db,
    )
    assert len(cal["interview_calendar"]) == 1
    assert list_calendar(db)[0]["meeting_link"].startswith("https://")

    lesson = add_lesson(
        app_id,
        {
            "interview_date": "2026-08-15",
            "stage": "phone_screen",
            "what_went_well": "Clear STAR on workflow automation",
            "what_to_improve": "Practice system design basics",
            "questions_asked": "Tell me about a workflow you built\nHow do you debug n8n?",
        },
        db,
    )
    assert len(lesson["lessons_learned"]) == 1

    # Empty offers — no fabrication
    empty = compare_offers(db)
    assert empty["count"] == 0
    assert empty["fabricated"] is False

    offer = update_offer(
        app_id,
        {
            "salary": 95000,
            "bonus": "10%",
            "benefits": "Health + 401k",
            "pto": "20 days",
            "remote_policy": "Fully remote US",
            "career_growth": "Path to Automation Specialist",
            "overall_score": 8,
        },
        db,
    )
    assert offer["offer"]["salary"] == 95000
    compared = compare_offers(db)
    assert compared["count"] == 1
    assert compared["offers"][0]["company"] == "GitLab"

    overview = assistant_overview(db)
    assert overview["fabricated"] is False
    assert overview["local_only"] is True
    assert len(overview["calendar"]) == 1
    assert len(overview["lessons"]) == 1
