from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Job
from app.services.career_agent import ALERT_SCORE_THRESHOLD, build_daily_brief, build_todays_brief
from app.services.filters import is_contract_or_commission_only, is_stale_listing, should_keep
from app.services.scorer import score_job


def _session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def test_scoring_v2_weights_and_no_invented_probability():
    job = {
        "title": "AI Operations Specialist",
        "company": "GitLab",
        "location": "Fully Remote (US)",
        "description": "Fully remote AI workflow automation with n8n, Airtable, Python. Entry level welcome. Career growth and mentorship.",
        "is_remote": True,
        "url": "https://about.gitlab.com/jobs/example",
        "salary_min": 80000,
        "salary_max": 100000,
        "tags": ["ai", "automation", "n8n"],
    }
    score, bd = score_job(job)
    assert 1 <= score <= 100
    assert bd["scoring_mode"] == "transparent_match_score_v2"
    assert bd["interview_probability"] is None
    assert abs(sum(bd["weights"].values()) - 1.0) < 1e-9
    assert bd["weights"]["skill_match"] == 0.35


def test_rejects_contract_only_and_stale():
    contract = {
        "title": "Support Engineer Contract Only",
        "company": "Zapier",
        "location": "Fully Remote",
        "description": "This is a contract-only role. Fully remote.",
        "url": "https://zapier.com/jobs/x",
        "is_remote": True,
    }
    assert is_contract_or_commission_only(contract) is True

    stale = {
        "title": "Automation Specialist",
        "company": "GitLab",
        "location": "Fully Remote",
        "description": "Fully remote automation.",
        "url": "https://about.gitlab.com/jobs/x",
        "posted_at": (datetime.utcnow() - timedelta(days=45)).isoformat(),
    }
    assert is_stale_listing(stale) is True
    stale["description"] += " Reposted this week."
    assert is_stale_listing(stale) is False


def test_todays_brief_and_90_alerts():
    db = _session()
    db.add(
        Job(
            external_id="t1",
            source="test",
            company="GitLab",
            title="AI Operations Specialist",
            location="Remote",
            url="https://example.com/1",
            description="Fully remote n8n",
            salary_text="$120,000",
            salary_min=120000,
            salary_max=130000,
            score=92,
            status="live",
            is_remote=1,
            found_at=datetime.utcnow(),
        )
    )
    db.add(
        Job(
            external_id="t2",
            source="test",
            company="Zapier",
            title="Support Engineer",
            location="Remote",
            url="https://example.com/2",
            description="Fully remote",
            score=81,
            status="live",
            is_remote=1,
            found_at=datetime.utcnow(),
        )
    )
    db.commit()
    today = build_todays_brief(db, refresh_log={"fetched": 10, "matched": 2})
    assert today["fabricated"] is False
    assert today["verified_remote_jobs"] == 2
    assert len(today["top_10_opportunities"]) == 2
    brief = build_daily_brief(db, refresh_log={"fetched": 10, "matched": 2, "top_10": []})
    assert any(n["type"] == "new_90_plus_matches" for n in brief["notifications"])
    assert ALERT_SCORE_THRESHOLD == 90.0


def test_keeps_priority_remote_target_role():
    job = {
        "title": "Junior Workflow Automation Specialist",
        "company": "GitLab",
        "location": "Fully Remote (US)",
        "description": "Build n8n and Airtable automations. Entry level welcome. Fully remote.",
        "is_remote": True,
        "url": "https://about.gitlab.com/jobs/all/",
        "tags": ["automation"],
    }
    assert should_keep(job) is True
