from __future__ import annotations

from app.services.source_policy import (
    is_allowed_free_source,
    is_paid_board_job,
    is_staffing_agency_without_employer,
)


def test_weworkremotely_blacklisted():
    paid, reason = is_paid_board_job(
        {
            "source": "weworkremotely",
            "url": "https://weworkremotely.com/remote-jobs/acme-support",
            "company": "Acme",
            "title": "Support Engineer",
            "description": "Remote",
        }
    )
    assert paid is True
    assert "paid" in reason
    allowed, _ = is_allowed_free_source(
        {
            "source": "weworkremotely",
            "url": "https://weworkremotely.com/remote-jobs/acme-support",
            "company": "Acme",
            "title": "Support",
            "description": "",
        }
    )
    assert allowed is False


def test_flexjobs_and_rocketship_blacklisted():
    assert is_paid_board_job(
        {
            "source": "manual",
            "url": "https://www.flexjobs.com/jobs/123",
            "company": "X",
            "title": "Remote Ops",
            "description": "",
        }
    )[0]
    assert is_paid_board_job(
        {
            "source": "remoterocketship",
            "url": "https://remoterocketship.com/jobs/1",
            "company": "Y",
            "title": "Engineer",
            "description": "Premium membership required to apply",
        }
    )[0]


def test_greenhouse_and_linkedin_allowed():
    assert is_allowed_free_source(
        {
            "source": "greenhouse:gitlab",
            "url": "https://boards.greenhouse.io/gitlab/jobs/1",
            "company": "GitLab",
            "title": "Support Engineer",
            "description": "Fully remote United States",
        }
    )[0]
    assert is_allowed_free_source(
        {
            "source": "linkedin",
            "url": "https://www.linkedin.com/jobs/view/123",
            "company": "Stripe",
            "title": "Solutions Engineer",
            "description": "Easy Apply",
        }
    )[0]
    assert is_allowed_free_source(
        {
            "source": "manual",
            "url": "https://careers.datadoghq.com/detail/123",
            "company": "Datadog",
            "title": "Technical Support Engineer",
            "description": "Remote US",
        }
    )[0]


def test_staffing_without_employer_blocked():
    assert is_staffing_agency_without_employer(
        {
            "company": "Apex Staffing Agency",
            "title": "Technical Support Engineer",
            "description": "We are a staffing agency seeking talent.",
            "url": "https://example-staffing.com/jobs/1",
            "source": "manual",
        }
    )
    assert not is_staffing_agency_without_employer(
        {
            "company": "Apex Staffing",
            "title": "Support Engineer",
            "description": "Hiring for our client Datadog on behalf of Datadog.",
            "url": "https://boards.greenhouse.io/datadog/jobs/1",
            "source": "greenhouse:datadog",
        }
    )


def test_search_jobs_does_not_register_wwr():
    import inspect

    from app.services import job_finder

    src = inspect.getsource(job_finder.search_jobs)
    assert "fetch_weworkremotely" not in src
    assert "fetch_greenhouse_board" in src
    assert "is_paid_board_job" in src
