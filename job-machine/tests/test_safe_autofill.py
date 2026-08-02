from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Application, Job
from app.services.safe_autofill import (
    classify_detected_fields,
    detect_platform,
    is_sensitive_question,
    mark_submitted,
    open_application_session,
    suggest_answer,
    verified_autofill_fields,
    verify_file_belongs_to_application,
)

FIXTURES = Path(__file__).resolve().parents[2] / "browser-extension" / "fixtures"


class InputParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.fields: list[dict] = []
        self._label = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "label":
            self._label = ""
        if tag in {"input", "textarea", "select"}:
            name = attrs.get("name", "")
            fid = attrs.get("id", "")
            label = self._label or name or fid
            mapped = None
            blob = f"{label} {name} {fid}"
            rules = [
                (r"first\s*name|firstName|first_name", "first_name"),
                (r"last\s*name|lastName|last_name", "last_name"),
                (r"full\s*name|^name$", "full_name"),
                (r"e-?mail", "email"),
                (r"phone", "phone"),
                (r"linkedin", "linkedin"),
                (r"github", "github"),
                (r"portfolio|website", "portfolio"),
                (r"city", "city"),
                (r"country", "country"),
                (r"state", "state"),
                (r"zip", "zip_code"),
                (r"title", "current_job_title"),
                (r"resume", "resume_file"),
                (r"cover", "cover_letter_file"),
            ]
            for pat, key in rules:
                if re.search(pat, blob, re.I):
                    mapped = key
                    break
            self.fields.append({"label": label, "name": name, "id": fid, "mapped_key": mapped})

    def handle_data(self, data):
        if data.strip():
            self._label = (self._label + " " + data.strip()).strip()


def _session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def _app(db):
    job = Job(
        external_id="af-1",
        source="greenhouse",
        company="GitLab",
        title="Technical Support Engineer",
        location="Remote",
        url="https://boards.greenhouse.io/gitlab/jobs/123",
        description="Remote support role",
        salary_text="$90,000",
    )
    db.add(job)
    db.commit()
    app = Application(
        job_id=job.id,
        company="GitLab",
        position="Technical Support Engineer",
        salary="$90,000",
        location="Remote",
        status="ready",
        tailored_resume="Leroy Garvin Jr\nAlignedVibesCo@gmail.com\n(912) 901-6378\nhttps://leroy-garvin-ai-portfolio.vercel.app\n",
        cover_letter="Dear GitLab team,\nI am interested in Technical Support Engineer.\nPortfolio: https://leroy-garvin-ai-portfolio.vercel.app\n",
        portfolio_refs='[{"name":"LawOne AI","url":"https://leroy-garvin-ai-portfolio.vercel.app"}]',
        application_score=70,
        analytics_json='{"resume_version":"B","cover_version":"A"}',
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


def test_platform_detection():
    assert detect_platform("https://boards.greenhouse.io/x/jobs/1") == "greenhouse"
    assert detect_platform("https://jobs.lever.co/x/abc") == "lever"
    assert detect_platform("https://jobs.ashbyhq.com/x") == "ashby"
    assert detect_platform("https://jobs.smartrecruiters.com/x") == "smartrecruiters"
    assert detect_platform("https://company.wd1.myworkdayjobs.com/en-US/careers") == "workday"
    assert detect_platform("https://apply.workable.com/x/j/1") == "workable"
    assert detect_platform("https://www.indeed.com/viewjob") == "indeed"
    assert detect_platform("https://www.linkedin.com/jobs/view/1") == "linkedin"
    assert detect_platform("https://careers.example.com/apply") == "generic"


def test_sensitive_questions_never_auto():
    assert is_sensitive_question("Will you require sponsorship?")
    assert is_sensitive_question("Desired salary")
    assert is_sensitive_question("Do you have a disability?")
    assert is_sensitive_question("Veteran status")
    assert is_sensitive_question("Are you authorized to work in the United States?")
    assert not is_sensitive_question("Why are you interested in this role?")


def test_verified_fields_exclude_street_and_null_zip():
    fields = verified_autofill_fields()
    assert fields["email"]
    assert fields["phone"]
    assert fields["linkedin"]
    assert fields["portfolio"]
    assert fields.get("zip_code") in (None, "")
    # street address must never be part of autofill keys
    assert "street_address" not in fields
    assert "home_address" not in fields


def test_fixture_field_mapping_and_sensitive_classification():
    for name in [
        "greenhouse.html",
        "lever.html",
        "ashby.html",
        "smartrecruiters.html",
        "workday.html",
        "workable.html",
        "indeed.html",
        "linkedin.html",
        "generic.html",
    ]:
        html = (FIXTURES / name).read_text(encoding="utf-8")
        parser = InputParser()
        parser.feed(html)
        assert parser.fields, f"No fields in {name}"
        classified = classify_detected_fields(parser.fields)
        assert classified["submit_buttons_will_not_be_clicked"] is True
        # Sensitive fields must be manual
        for item in classified["sensitive_manual"]:
            assert item["action"] == "manual_only"
        # At least email or name should be autofillable on most fixtures
        if name != "linkedin.html":
            keys = {x.get("mapped_key") for x in classified["autofill_candidates"]}
            assert keys & {"email", "first_name", "last_name", "full_name", "phone"}


def test_wrong_company_file_rejected():
    db = _session()
    app = _app(db)
    assert verify_file_belongs_to_application(app.id, "GitLab_Technical-Support-Engineer_resume.md", db)
    assert not verify_file_belongs_to_application(app.id, "Acme_Other-Role_resume.md", db)


def test_open_session_requires_confirm_never_autosubmit():
    db = _session()
    app = _app(db)
    payload = open_application_session(app.id, db)
    assert payload["auto_submit"] is False
    assert payload["requires_confirm_autofill"] is True
    assert payload["never_click_submit"] is True
    assert payload["captcha_bypass"] is False
    assert payload["platform"] == "greenhouse"
    assert payload["fillable_fields"]["email"]
    assert "zip_code" not in payload["fillable_fields"]


def test_suggest_answer_sensitive_blank_and_draft_requires_review():
    db = _session()
    app = _app(db)
    sens = suggest_answer(app.id, "Will you now or in the future require sponsorship?", db)
    assert sens["suggested_answer"] is None
    assert sens["auto_fill"] is False
    draft = suggest_answer(app.id, "Why are you interested in this role?", db)
    assert draft["suggested_answer"]
    assert draft["requires_review"] is True
    assert draft["auto_fill"] is False
    assert draft["label"] == "Suggested Answer"
    assert draft["source_facts"]


def test_mark_submitted_tracking():
    db = _session()
    app = _app(db)
    result = mark_submitted(
        app.id,
        db,
        application_url="https://boards.greenhouse.io/gitlab/jobs/123",
        platform="greenhouse",
        notes="Submitted manually",
    )
    assert result["auto_submit"] is False
    assert result["submission"]["company"] == "GitLab"
    assert result["submission"]["role"] == "Technical Support Engineer"
    assert result["submission"]["platform"] == "greenhouse"
    assert result["submission"]["follow_up_date"]
    db.refresh(app)
    assert app.status == "applied"
    assert app.date_applied is not None


def test_never_click_submit_contract_in_extension_safety_js():
    safety = Path(__file__).resolve().parents[2] / "browser-extension" / "lib" / "safety.js"
    text = safety.read_text(encoding="utf-8")
    assert "neverClickSubmit" in text
    assert "return false" in text
    content = (Path(__file__).resolve().parents[2] / "browser-extension" / "content" / "content.js").read_text(
        encoding="utf-8"
    )
    assert "Confirm Autofill" in content
    assert "Yes — Mark Applied" in content or "Mark Applied" in content
    assert "READY FOR FINAL REVIEW" in content
    assert "Submit was NOT clicked" in content or "Submit will NOT" in content
