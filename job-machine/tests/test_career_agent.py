from __future__ import annotations

from datetime import date, datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Application, Job, RecruiterContact
from app.services.career_agent import HIGH_SCORE_THRESHOLD, build_daily_brief, save_daily_brief
from app.services.career_coach import analyze_career, weekly_improvement_report
from app.services.interview_intelligence import generate_interview_intelligence
from app.services.recruiter_crm import import_from_applications, list_contacts, upsert_contact


def _session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def _seed(db):
    j1 = Job(
        external_id="c1",
        source="test",
        company="GitLab",
        title="Technical Support Engineer",
        location="Remote",
        url="https://boards.greenhouse.io/gitlab/jobs/1",
        description="Fully remote. Use n8n, Airtable, Python, SQL, Zendesk. Competitors include Acme Tools. Series B $50M. Recently announced new support hub.",
        salary_text="$85,000 – $95,000",
        salary_min=85000,
        salary_max=95000,
        tags="support,n8n,python",
        score=86,
        status="live",
        found_at=datetime.utcnow(),
    )
    j2 = Job(
        external_id="c2",
        source="test",
        company="GitLab",
        title="Automation Specialist",
        location="Remote",
        url="https://example.com/2",
        description="Remote automation with Zapier and APIs. Apply by 2099-01-01.",
        salary_min=70000,
        salary_max=90000,
        tags="automation,zapier",
        score=72,
        status="live",
        found_at=datetime.utcnow() - timedelta(days=2),
    )
    db.add_all([j1, j2])
    db.commit()
    app = Application(
        job_id=j1.id,
        company="GitLab",
        position="Technical Support Engineer",
        salary="$90,000",
        status="recruiter_viewed",
        recruiter_name="Alex Recruiter",
        recruiter_email="alex@example.com",
        follow_up_date=date.today(),
        interview_date=date.today() + timedelta(days=3),
        tailored_resume="Leroy Garvin Jr portfolio https://leroy-garvin-ai-portfolio.vercel.app",
        cover_letter="Interest in GitLab support",
        portfolio_refs='[{"name":"GH-X Automation System","id":"ghx","blurb":"n8n Airtable pipeline","metrics":["10 stages"]}]',
        application_score=86,
        analytics_json="{}",
    )
    db.add(app)
    db.commit()
    db.refresh(j1)
    db.refresh(app)
    return j1, app


def test_daily_brief_truthful_and_high_score_notify():
    db = _session()
    _seed(db)
    brief = build_daily_brief(db, refresh_log={"fetched": 2, "matched": 2, "added": 1, "packets_prepared": 1, "top_10": []})
    assert brief["fabricated"] is False
    assert brief["auto_apply"] is False
    assert brief["auto_email"] is False
    assert brief["notify_threshold"] == HIGH_SCORE_THRESHOLD
    assert any(b["score"] >= 80 and b["notify"] for b in brief["best_opportunities"])
    assert any(n["type"] == "high_match_jobs" for n in brief["notifications"])
    assert brief["companies_hiring_repeatedly"][0]["company"] == "GitLab"
    assert brief["salary_trends"]["samples"] >= 1
    assert brief["recruiters_viewing_applications"]
    assert brief["follow_ups_due_today"]
    assert brief["upcoming_interviews"]
    # certs never claimed as held
    assert all(c.get("held_by_leroy") is False for c in brief["recommended_certifications"])
    path = save_daily_brief(brief)
    assert path.exists()


def test_career_coach_does_not_invent_certs():
    db = _session()
    _seed(db)
    analysis = analyze_career(db)
    assert analysis["fabricated"] is False
    assert analysis["profile_truth"]["certifications_listed"] == []
    report = weekly_improvement_report(db)
    assert report["approval_required"] is True
    assert report["auto_email"] is False
    assert report["recommended_actions"]


def test_recruiter_crm_no_auto_email():
    db = _session()
    _seed(db)
    contact = upsert_contact(
        db,
        {
            "recruiter_name": "Pat Talent",
            "company": "Zapier",
            "email": "pat@example.com",
            "phone": "555-0100",
            "linkedin": "https://www.linkedin.com/in/example",
            "last_contact": date.today().isoformat(),
            "follow_up_date": (date.today() + timedelta(days=2)).isoformat(),
            "notes": "Met at virtual fair",
            "referral_opportunities": "Ask about Automation Specialist team",
        },
    )
    assert contact["auto_email"] is False
    assert contact["approval_required_for_outreach"] is True
    imported = import_from_applications(db)
    assert imported["created"] >= 1
    assert imported["auto_email"] is False
    assert len(list_contacts(db)) >= 2
    assert db.query(RecruiterContact).count() >= 2


def test_interview_intelligence_no_fabricated_finance_when_absent():
    db = _session()
    job = Job(
        external_id="plain",
        source="test",
        company="ExampleOps",
        title="AI Operations Associate",
        location="Remote",
        url="https://example.com/job",
        description="Remote AI operations role using n8n and documentation. Fully remote collaborative team.",
        tags="n8n,ops",
        score=70,
        status="live",
    )
    db.add(job)
    db.commit()
    intel = generate_interview_intelligence(None, job.id, db)
    assert intel["fabricated"] is False
    assert intel["auto_email"] is False
    assert intel["financial_overview"]["available"] is False
    assert "not invent" in intel["financial_overview"]["note"].lower()
    assert "unavailable" in intel["competitors"][0].lower() or "fabricate" in intel["competitors"][0].lower()
    assert intel["elevator_pitch_30s"]
    assert "Leroy" in intel["elevator_pitch_30s"]
    assert intel["star_answers"] is not None
    assert intel["approval_required"] is True


def test_interview_intelligence_extracts_posting_facts_only():
    db = _session()
    j1, app = _seed(db)
    intel = generate_interview_intelligence(app.id, j1.id, db)
    assert intel["financial_overview"]["available"] is True
    assert any("50M" in f or "Series" in f for f in intel["financial_overview"]["figures"])
    assert intel["latest_news"]["available"] is True
    assert any("n8n" in t.lower() or "support" in t.lower() for t in intel["technical_topics_likely"])
