from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from app.config import ROOT
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
from app.services.filters import load_profile
from app.services.pipeline_stages import PORTFOLIO_URL

PACKETS_DIR = ROOT / "data" / "interview_packets"


def _safe(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", name).strip("-")[:80] or "packet"


def packet_dir(job_id: int, company: str = "", title: str = "") -> Path:
    label = _safe(f"{job_id}-{company}-{title}")
    path = PACKETS_DIR / label
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_packet_locally(
    *,
    job_id: int,
    company: str,
    title: str,
    resume: str,
    cover: str,
    prep: dict[str, Any],
    projects: list[dict[str, Any]],
    why_match: str,
    interview_probability: float,
    match_percentage: float,
    estimated_salary: str,
    status: str = "ready",
) -> dict[str, str]:
    """Persist resume, cover (md/pdf/docx), prep, and meta under data/interview_packets/."""
    profile = load_profile()
    folder = packet_dir(job_id, company, title)

    docs = write_ats_packet_documents(
        folder,
        resume_markdown=resume,
        cover_markdown=cover,
        company=company,
        title=title,
    )

    (folder / "interview_prep.json").write_text(json.dumps(prep, indent=2), encoding="utf-8")

    from app.services.interview_prep import render_prep_markdown

    prep_md = render_prep_markdown(prep, {"title": title, "company": company})
    (folder / "interview_prep.md").write_text(prep_md, encoding="utf-8")

    zip_path = build_packet_zip(folder)

    meta = {
        "job_id": job_id,
        "company": company,
        "title": title,
        "status": status,
        "approval_required": True,
        "auto_apply": False,
        "interview_probability": interview_probability,
        "match_percentage": match_percentage,
        "estimated_salary": estimated_salary,
        "why_match": why_match,
        "portfolio_url": profile["candidate"].get("portfolio") or PORTFOLIO_URL,
        "projects": projects,
        "saved_at": datetime.utcnow().isoformat() + "Z",
        "preferred_resume": docs.get("preferred_resume"),
        "preferred_cover": docs.get("preferred_cover"),
        "ats_export": {
            "pdf_ok": docs.get("pdf_ok"),
            "docx_ok": docs.get("docx_ok"),
            "fallback_used": docs.get("fallback_used"),
            "files_written": docs.get("files_written"),
        },
        "paths": {
            "resume": str(folder / RESUME_MD),
            "cover_letter": str(folder / COVER_MD),
            "resume_pdf": docs["paths"].get("resume_pdf"),
            "cover_pdf": docs["paths"].get("cover_pdf"),
            "resume_docx": docs["paths"].get("resume_docx"),
            "cover_docx": docs["paths"].get("cover_docx"),
            "export_zip": str(zip_path),
            "interview_prep_json": str(folder / "interview_prep.json"),
            "interview_prep_md": str(folder / "interview_prep.md"),
        },
    }
    (folder / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return {k: v for k, v in meta["paths"].items() if v}


def load_packet_meta(job_id: int) -> dict[str, Any] | None:
    if not PACKETS_DIR.exists():
        return None
    for folder in PACKETS_DIR.iterdir():
        if not folder.is_dir():
            continue
        if not folder.name.startswith(f"{job_id}-"):
            continue
        meta_path = folder / "meta.json"
        if meta_path.exists():
            return json.loads(meta_path.read_text(encoding="utf-8"))
    return None


def export_bundle_files(
    *,
    resume: str,
    cover: str,
    portfolio_url: str,
    company: str,
    title: str,
    job_id: int | None = None,
    application_id: int | None = None,
) -> dict[str, Any]:
    """Generate md+pdf+docx into the job packet folder and return one-click export payload."""
    folder_id = job_id if job_id is not None else (application_id or 0)
    folder = packet_dir(folder_id, company, title)
    docs = write_ats_packet_documents(
        folder,
        resume_markdown=resume,
        cover_markdown=cover,
        company=company,
        title=title,
    )
    zip_path = build_packet_zip(folder)

    # Keep company-tagged copies for legacy autofill token checks
    tagged_resume = folder / f"{_safe(company)}_{_safe(title)}_resume.md"
    tagged_cover = folder / f"{_safe(company)}_{_safe(title)}_cover.md"
    tagged_resume.write_text(resume or "", encoding="utf-8")
    tagged_cover.write_text(cover or "", encoding="utf-8")

    base = ""
    if application_id:
        base = f"/api/applications/{application_id}/export"
    elif job_id is not None:
        base = f"/api/jobs/{job_id}/export"
    else:
        base = ""

    files = {
        RESUME_MD: str(folder / RESUME_MD),
        RESUME_PDF: docs["paths"].get("resume_pdf"),
        RESUME_DOCX: docs["paths"].get("resume_docx"),
        COVER_MD: str(folder / COVER_MD),
        COVER_PDF: docs["paths"].get("cover_pdf"),
        COVER_DOCX: docs["paths"].get("cover_docx"),
        "export_packet.zip": str(zip_path),
    }

    download_urls = {}
    if base:
        download_urls = {
            RESUME_MD: f"{base}/file/{RESUME_MD}",
            RESUME_PDF: f"{base}/file/{RESUME_PDF}",
            RESUME_DOCX: f"{base}/file/{RESUME_DOCX}",
            COVER_MD: f"{base}/file/{COVER_MD}",
            COVER_PDF: f"{base}/file/{COVER_PDF}",
            COVER_DOCX: f"{base}/file/{COVER_DOCX}",
            "zip": f"{base}/zip",
        }

    preferred_resume = docs.get("preferred_resume") or RESUME_PDF
    preferred_cover = docs.get("preferred_cover") or COVER_PDF

    return {
        "resume_filename": RESUME_MD,
        "cover_filename": COVER_MD,
        "resume": resume,
        "cover_letter": cover,
        "portfolio_url": portfolio_url or PORTFOLIO_URL,
        "export_note": (
            "ATS packet ready (md + pdf + docx). PDF preferred for upload; DOCX used if PDF fails. "
            "Applications require Leroy's approval — never auto-submitted."
        ),
        "folder": str(folder),
        "files": {k: v for k, v in files.items() if v},
        "files_written": docs.get("files_written") or [],
        "download_urls": download_urls,
        "zip_url": download_urls.get("zip"),
        "preferred_resume": preferred_resume,
        "preferred_cover": preferred_cover,
        "preferred_resume_url": download_urls.get(preferred_resume),
        "preferred_cover_url": download_urls.get(preferred_cover),
        "pdf_ok": bool(docs.get("pdf_ok")),
        "docx_ok": bool(docs.get("docx_ok")),
        "fallback_used": bool(docs.get("fallback_used")),
    }
