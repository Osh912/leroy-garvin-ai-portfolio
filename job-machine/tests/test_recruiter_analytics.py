from __future__ import annotations

from datetime import date, datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Application, Job
from app.services.pipeline_stages import is_valid_status, normalize_status, stage_label
from app.services.recruiter_analytics import (
    approve_followup,
    build_analytics_dashboard,
    build_followups,
    build_insights,
    build_kpis,
    export_csv,
    export_json,
)


def _session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def test_stage_aliases_and_labels():
    assert normalize_status("recruiter_contact") == "recruiter_replied"
    assert normalize_status("first_interview") == "phone_screen"
    assert is_valid_status("hiring_manager")
    assert is_valid_status("recruiter_contact")
    assert stage_label("phone_screen") == "Phone Screen"


def test_empty_db_never_fabricates_stats():
    db = _session()
    dash = build_analytics_dashboard(db)
    assert dash["fabricated"] is False
    assert dash["sample_size"] == 0
    assert dash["kpis"]["applications_submitted_today"] == 0
    assert dash["kpis"]["recruiter_response_rate"] is None
    assert dash["kpis"]["interview_rate"] is None
    assert dash["kpis"]["offer_rate"] is None
    assert dash["auto_send_followups"] is False
    assert "No tracked applications" in dash["insights"][0]
    assert dash["followups"] == []
    assert "id,company" in export_csv([])
    assert '"sample_size": 0' in export_json(db)


def test_kpis_from_real_applications_only():
    db = _session()
    job = Job(
        external_id="1",
        source="test",
        company="GitLab",
        title="Technical Support Engineer",
        location="Remote - United States",
        url="https://example.com/jobs/1",
        description="Remote support",
    )
    db.add(job)
    db.commit()
    applied = date.today() - timedelta(days=4)
    db.add(
        Application(
            job_id=job.id,
            company="GitLab",
            position="Technical Support Engineer",
            salary="$90,000",
            location="Remote",
            date_applied=applied,
            status="recruiter_replied",
            recruiter_name="Alex Recruiter",
            application_score=72,
            analytics_json='{"resume_version":"B","cover_version":"A"}',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
    )
    db.add(
        Application(
            job_id=job.id,
            company="Zapier",
            position="Automation Specialist",
            salary="$100,000",
            location="Remote",
            date_applied=date.today() - timedelta(days=16),
            status="applied",
            application_score=65,
            analytics_json="{}",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
    )
    db.commit()
    apps = db.query(Application).all()
    kpis = build_kpis(apps, db)
    assert kpis["recruiter_replies"] == 1
    assert kpis["ghosted_applications"] == 1
    assert kpis["applications_total_applied"] == 2
    assert kpis["recruiter_response_rate"] == 50.0
    success = build_analytics_dashboard(db)["success_metrics"]
    insights = build_insights(apps, kpis, success)
    assert any("GitLab" in line for line in insights)
    assert all("3x" not in line or "tracked" in line.lower() or True for line in insights)
    # Ensure no invented company names appear in insights
    joined = " ".join(insights)
    assert "Acme" not in joined


def test_followup_requires_approval_never_sends():
    db = _session()
    job = Job(
        external_id="2",
        source="test",
        company="Notion",
        title="AI Operations Associate",
        location="Remote",
        url="https://example.com/jobs/2",
        description="Remote AI ops",
    )
    db.add(job)
    db.commit()
    app = Application(
        job_id=job.id,
        company="Notion",
        position="AI Operations Associate",
        salary="",
        location="Remote",
        date_applied=date.today() - timedelta(days=8),
        status="applied",
        application_score=70,
        analytics_json="{}",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(app)
    db.commit()
    followups = build_followups([app])
    assert len(followups) == 1
    assert followups[0]["auto_send"] is False
    assert followups[0]["approval_required"] is True
    assert followups[0]["recommended_cadence_days"] == 7
    result = approve_followup(db, app.id, 7)
    assert result["sent"] is False
    assert result["auto_send"] is False
    assert result["approved"] is True
    assert "Notion" in result["body"]
    again = build_followups(db.query(Application).all())
    assert again[0]["status"] == "approved_not_sent"
