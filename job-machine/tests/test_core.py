from __future__ import annotations

from app.services.filters import should_keep
from app.services.portfolio_matcher import match_portfolio
from app.services.scorer import score_job
from app.services.truth_guard import scan_for_fabrication


def test_keeps_remote_automation_role():
    job = {
        "title": "Junior Workflow Automation Specialist",
        "company": "GitLab",
        "location": "Remote - United States",
        "description": "Build n8n and Airtable automations. Entry level welcome. Fully remote.",
        "is_remote": True,
        "url": "https://about.gitlab.com/jobs/all/",
        "tags": ["automation"],
    }
    assert should_keep(job) is True


def test_rejects_city_without_explicit_remote():
    from app.services.filters import verify_remote

    job = {
        "title": "Technical Support Engineer",
        "company": "stripe",
        "location": "San Francisco, CA",
        "description": "Support customers. Some remote flexibility.",
        "source": "greenhouse:stripe",
        "tags": ["support"],
    }
    v = verify_remote(job)
    assert v["verified"] is False
    assert "✗" in v["label"]
    assert should_keep(job) is False


def test_accepts_city_with_fully_remote_marker():
    from app.services.filters import verify_remote

    job = {
        "title": "Junior Automation Specialist",
        "company": "Zapier",
        "location": "Fully Remote (US)",
        "description": "Build n8n-style workflows. Entry level welcome. 100% Remote.",
        "source": "greenhouse:zapier",
        "salary_min": 70000,
        "tags": ["automation", "n8n"],
    }
    v = verify_remote(job)
    assert v["verified"] is True
    assert "✓" in v["label"]


def test_rejects_hybrid():
    from app.services.filters import verify_remote

    job = {
        "title": "Support Specialist",
        "company": "Zapier",
        "location": "Hybrid - Boston",
        "description": "Hybrid role with office days.",
        "tags": ["support"],
    }
    assert verify_remote(job)["verified"] is False


def test_rejects_onsite_unrelated():
    job = {
        "title": "Restaurant Manager",
        "company": "Local Diner",
        "location": "Savannah, GA",
        "description": "Manage restaurant staff on site daily.",
        "is_remote": False,
        "tags": [],
    }
    assert should_keep(job) is False


def test_score_range():
    job = {
        "title": "AI Operations Specialist",
        "company": "GitLab",
        "location": "Remote USA",
        "description": "Own AI workflow automation, prompt QA, n8n, Airtable, technical support. Fully remote.",
        "is_remote": True,
        "url": "https://about.gitlab.com/jobs/example",
        "salary_min": 75000,
        "salary_max": 95000,
        "tags": ["ai", "automation"],
    }
    score, breakdown = score_job(job)
    assert 1 <= score <= 100
    assert "skill_match" in breakdown
    assert "resume_match" in breakdown
    assert "portfolio_match" in breakdown
    assert breakdown["weights"]["skill_match"] == 0.25
    assert breakdown.get("interview_probability") is None
    assert breakdown["scoring_mode"] == "transparent_match_score_v1"


def test_blocks_placeholder_company():
    from app.services.production import is_placeholder_company, is_production_eligible

    assert is_placeholder_company("Acme AI") is True
    assert is_placeholder_company("Example Corp") is True
    ok, reason = is_production_eligible(
        {"company": "Acme AI", "title": "Ops", "url": "https://example.com/job"}
    )
    assert ok is False
    assert reason == "placeholder_company"


def test_rejects_below_salary_floor():
    job = {
        "title": "Junior Automation Specialist",
        "company": "Zapier",
        "location": "Remote, United States",
        "description": "Build n8n workflows. Entry level welcome. Fully remote.",
        "is_remote": True,
        "url": "https://zapier.com/jobs/position/test",
        "salary_min": 40000,
        "salary_max": 48000,
        "tags": ["automation", "n8n"],
    }
    assert should_keep(job) is False


def test_rejects_hard_bachelors():
    job = {
        "title": "Junior Automation Specialist",
        "company": "Zapier",
        "location": "Remote, United States",
        "description": "Build n8n workflows. Bachelor's degree required. Entry level welcome. Fully remote.",
        "is_remote": True,
        "url": "https://zapier.com/jobs/position/test",
        "salary_min": 70000,
        "tags": ["automation", "n8n"],
    }
    assert should_keep(job, prefer_no_degree=True) is False
    assert should_keep(job, prefer_no_degree=False) is True


def test_quick_filter_python():
    from app.services.filters import matches_quick_filters

    job = {
        "title": "Technical Support Associate",
        "company": "Zapier",
        "location": "Remote, United States",
        "description": "Support customers using Python scripts and workflows.",
        "tags": [],
    }
    assert matches_quick_filters(job, ["Python"]) is True
    assert matches_quick_filters(job, ["n8n"]) is False


def test_portfolio_match_prefers_automation_stack():
    job = {
        "title": "Automation Specialist",
        "company": "Zapier",
        "location": "Remote",
        "description": "n8n workflows, Airtable ops, implementation support",
        "tags": [],
    }
    matched = match_portfolio(job)
    ids = {m["id"] for m in matched}
    assert ids & {"ghx", "n8n", "airtable"}


def test_rejects_hard_five_years():
    job = {
        "title": "Automation Specialist",
        "company": "Zapier",
        "location": "Remote, United States",
        "description": "Requires 5+ years of experience building automations. Fully remote.",
        "is_remote": True,
        "url": "https://zapier.com/jobs/position/test",
        "tags": ["automation"],
    }
    assert should_keep(job) is False


def test_allows_preferred_five_years():
    job = {
        "title": "Junior Automation Specialist",
        "company": "Zapier",
        "location": "Remote, United States",
        "description": "Build n8n workflows and Airtable ops. 5+ years preferred. Fully remote.",
        "is_remote": True,
        "url": "https://zapier.com/jobs/position/test",
        "tags": ["automation", "n8n"],
    }
    assert should_keep(job) is True


def test_interview_prep_has_required_sections():
    from app.services.interview_prep import build_interview_prep

    job = {
        "title": "Technical Support Engineer",
        "company": "GitLab",
        "location": "Remote, United States",
        "description": "Support customers using automation workflows. Fully remote.",
        "salary_text": "$80,000-$100,000",
        "tags": ["support"],
    }
    projects = [
        {
            "id": "ghx",
            "name": "GH-X Automation System",
            "url": "https://leroy-garvin-ai-portfolio.vercel.app/projects/ghx.html",
            "blurb": "23 n8n workflows",
            "metrics": ["23 workflows"],
        }
    ]
    prep = build_interview_prep(job, projects, why_match="Strong support + automation overlap")
    assert prep["likely_interview_questions"]
    assert prep["technical_questions"]
    assert prep["behavioral_questions"]
    assert prep["star_answers"]
    assert prep["company_research"]
    assert prep["recruiter_cheat_sheet"]
    assert prep["salary_information"]
    assert prep["questions_leroy_should_ask"]
    assert prep["portfolio_url"]


def test_pipeline_stages_include_interview_path():
    from app.services.pipeline_stages import PIPELINE_STAGES

    for stage in [
        "saved",
        "ready",
        "applied",
        "recruiter_contact",
        "first_interview",
        "technical_interview",
        "final_interview",
        "offer",
        "rejected",
    ]:
        assert stage in PIPELINE_STAGES


def test_truth_guard_flags_senior_engineer():
    warnings = scan_for_fabrication("I am a senior engineer with a PhD in computer science.")
    assert warnings
