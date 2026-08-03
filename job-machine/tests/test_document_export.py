from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Application, Job
from app.services.document_export import (
    COVER_DOCX,
    COVER_MD,
    COVER_PDF,
    RESUME_DOCX,
    RESUME_MD,
    RESUME_PDF,
    build_packet_zip,
    write_ats_packet_documents,
)
from app.services.packet_store import export_bundle_files
from app.services.safe_autofill import ensure_application_files


SAMPLE_RESUME = """# Leroy Garvin Jr
AI Automation | AI Operations | Workflow Automation
Savannah, Georgia, USA · Open to Remote
(912) 901-6378 · AlignedVibesCo@gmail.com

## Professional summary
Owner and AI Operations Specialist at Right Outside Auto Detailing LLC.

## Core skills
AI Workflow Design · Prompt Engineering · n8n · Airtable

## Experience
### Owner & AI Operations Specialist
Right Outside Auto Detailing LLC — Present
- Design AI-assisted booking workflows
- Build no-code automation with n8n and Airtable
"""

SAMPLE_COVER = """# Cover Letter
Dear Hiring Team,

I am applying for the Technical Support Engineer role at GitLab.

Portfolio: https://leroy-garvin-ai-portfolio.vercel.app

Sincerely,
Leroy Garvin Jr
"""

FIXTURES = Path(__file__).resolve().parents[2] / "browser-extension" / "fixtures"


def _session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def test_write_ats_packet_creates_md_pdf_docx(tmp_path: Path):
    docs = write_ats_packet_documents(
        tmp_path,
        resume_markdown=SAMPLE_RESUME,
        cover_markdown=SAMPLE_COVER,
        company="GitLab",
        title="Technical Support Engineer",
    )
    for name in (RESUME_MD, RESUME_PDF, RESUME_DOCX, COVER_MD, COVER_PDF, COVER_DOCX):
        assert (tmp_path / name).exists(), name
        assert (tmp_path / name).stat().st_size > 100, name
    assert docs["preferred_resume"] == RESUME_PDF
    assert docs["preferred_cover"] == COVER_PDF
    assert docs["pdf_ok"] is True
    assert docs["docx_ok"] is True
    assert docs["fallback_used"] is False
    zip_path = build_packet_zip(tmp_path)
    assert zip_path.exists()
    assert zip_path.stat().st_size > 200


def test_export_bundle_one_click_formats():
    db = _session()
    job = Job(
        external_id="exp-1",
        source="greenhouse",
        company="GitLab",
        title="Technical Support Engineer",
        location="Remote",
        url="https://boards.greenhouse.io/gitlab/jobs/1",
        description="Remote",
        salary_text="$90k",
    )
    db.add(job)
    db.commit()
    app = Application(
        job_id=job.id,
        company="GitLab",
        position="Technical Support Engineer",
        status="ready",
        tailored_resume=SAMPLE_RESUME,
        cover_letter=SAMPLE_COVER,
        application_score=80,
    )
    db.add(app)
    db.commit()
    db.refresh(app)

    bundle = export_bundle_files(
        resume=SAMPLE_RESUME,
        cover=SAMPLE_COVER,
        portfolio_url="https://leroy-garvin-ai-portfolio.vercel.app",
        company="GitLab",
        title="Technical Support Engineer",
        job_id=job.id,
        application_id=app.id,
    )
    assert bundle["pdf_ok"] is True
    assert bundle["docx_ok"] is True
    assert RESUME_PDF in bundle["files_written"]
    assert COVER_DOCX in bundle["files_written"]
    assert bundle["zip_url"]
    assert bundle["preferred_resume"] == RESUME_PDF
    folder = Path(bundle["folder"])
    assert (folder / RESUME_MD).exists()
    assert (folder / RESUME_PDF).exists()
    assert (folder / RESUME_DOCX).exists()
    assert (folder / COVER_MD).exists()
    assert (folder / COVER_PDF).exists()
    assert (folder / COVER_DOCX).exists()

    files = ensure_application_files(app, job)
    assert files["resume_pdf"]
    assert files["resume_docx"]
    assert files["preferred_resume"] == RESUME_PDF


def test_pdf_fallback_raises_when_pdf_fails(monkeypatch, tmp_path: Path):
    import app.services.document_export as de
    from app.services.document_export import ExportGenerationError

    def fail_pdf(*_a, **_k):
        raise RuntimeError("simulated PDF engine failure")

    monkeypatch.setattr(de, "write_markdown_pdf", fail_pdf)
    try:
        de.write_ats_packet_documents(
            tmp_path,
            resume_markdown=SAMPLE_RESUME,
            cover_markdown=SAMPLE_COVER,
            company="Acme",
            title="Support",
            require_all=True,
        )
        assert False, "should have raised"
    except ExportGenerationError as exc:
        assert any("resume.pdf" in e for e in exc.errors)
        assert "simulated PDF engine failure" in str(exc)
    # With require_all=False, still records errors and prefers nothing incomplete
    docs = de.write_ats_packet_documents(
        tmp_path,
        resume_markdown=SAMPLE_RESUME,
        cover_markdown=SAMPLE_COVER,
        company="Acme",
        title="Support",
        require_all=False,
    )
    assert docs["success"] is False
    assert docs["pdf_ok"] is False
    assert (tmp_path / RESUME_DOCX).exists()
    assert any("simulated PDF" in e for e in docs["errors"])


def test_fixtures_still_have_file_inputs_for_ats_platforms():
    for name in [
        "greenhouse.html",
        "lever.html",
        "ashby.html",
        "smartrecruiters.html",
        "workday.html",
        "generic.html",
    ]:
        html = (FIXTURES / name).read_text(encoding="utf-8")
        assert 'type="file"' in html or "type='file'" in html, name
    # Extension attaches preferred PDF by default
    content = (
        Path(__file__).resolve().parents[2] / "browser-extension" / "content" / "content.js"
    ).read_text(encoding="utf-8")
    assert "Attach Resume (PDF)" in content
    api = (Path(__file__).resolve().parents[2] / "browser-extension" / "lib" / "api.js").read_text(
        encoding="utf-8"
    )
    assert "fetchPreferredFile" in api
    assert '["pdf", "docx", "md"]' in api or '"pdf"' in api
