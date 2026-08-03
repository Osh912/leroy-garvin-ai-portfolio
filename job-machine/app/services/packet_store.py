from __future__ import annotations

import json
import logging
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
    STANDARD_PACKET_FILES,
    ExportGenerationError,
    build_packet_zip,
    write_ats_packet_documents,
)
from app.services.filters import load_profile
from app.services.pipeline_stages import PORTFOLIO_URL

log = logging.getLogger("job_machine.export")

PACKETS_DIR = ROOT / "data" / "interview_packets"


def _safe(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", name).strip("-")[:80] or "packet"


def packet_dir(job_id: int, company: str = "", title: str = "") -> Path:
    label = _safe(f"{job_id}-{company}-{title}")
    path = (PACKETS_DIR / label).resolve()
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
        require_all=True,
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
        "absolute_folder": str(folder),
        "ats_export": {
            "pdf_ok": docs.get("pdf_ok"),
            "docx_ok": docs.get("docx_ok"),
            "files_written": docs.get("files_written"),
            "verified_on_disk": docs.get("verified_on_disk"),
            "errors": docs.get("errors"),
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
    """Generate all six ATS files into the job packet folder. Raises if PDF/DOCX missing."""
    folder_id = job_id if job_id is not None else (application_id or 0)
    folder = packet_dir(folder_id, company, title)
    log.info(
        "export.bundle start application_id=%s job_id=%s folder=%s",
        application_id,
        job_id,
        folder,
    )

    try:
        docs = write_ats_packet_documents(
            folder,
            resume_markdown=resume,
            cover_markdown=cover,
            company=company,
            title=title,
            require_all=True,
        )
    except ExportGenerationError:
        raise
    except Exception as exc:  # noqa: BLE001
        log.exception("export.bundle unexpected failure")
        raise ExportGenerationError(
            f"Export failed: {type(exc).__name__}: {exc}",
            errors=[f"{type(exc).__name__}: {exc}"],
            folder=str(folder),
        ) from exc

    zip_path = build_packet_zip(folder)

    # Keep company-tagged markdown copies for legacy helpers
    tagged_resume = folder / f"{_safe(company)}_{_safe(title)}_resume.md"
    tagged_cover = folder / f"{_safe(company)}_{_safe(title)}_cover.md"
    tagged_resume.write_text(resume or "", encoding="utf-8")
    tagged_cover.write_text(cover or "", encoding="utf-8")

    base = ""
    if application_id:
        base = f"/api/applications/{application_id}/export"
    elif job_id is not None:
        base = f"/api/jobs/{job_id}/export"

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

    files_on_disk = {
        name: str(folder / name)
        for name in STANDARD_PACKET_FILES
        if (folder / name).exists()
    }
    # Hard verify again before reporting success
    missing = [n for n in STANDARD_PACKET_FILES if n not in files_on_disk]
    if missing:
        raise ExportGenerationError(
            f"Post-write verification failed — missing {missing} in {folder}",
            errors=docs.get("errors") or [],
            folder=str(folder),
        )

    log.info("export.bundle SUCCESS absolute_folder=%s files=%s", folder, list(files_on_disk))

    return {
        "resume_filename": RESUME_PDF,  # prefer PDF name in UI (not .md)
        "cover_filename": COVER_PDF,
        "resume": resume,
        "cover_letter": cover,
        "portfolio_url": portfolio_url or PORTFOLIO_URL,
        "export_note": (
            f"ATS packet complete (6 files) at {folder}. "
            "Applications require Leroy's approval — never auto-submitted."
        ),
        "folder": str(folder),
        "absolute_folder": str(folder),
        "files": files_on_disk,
        "files_written": list(STANDARD_PACKET_FILES),
        "missing_files": [],
        "verified_on_disk": docs.get("verified_on_disk") or {},
        "download_urls": download_urls,
        "zip_url": download_urls.get("zip"),
        "preferred_resume": RESUME_PDF,
        "preferred_cover": COVER_PDF,
        "preferred_resume_url": download_urls.get(RESUME_PDF),
        "preferred_cover_url": download_urls.get(COVER_PDF),
        "pdf_ok": True,
        "docx_ok": True,
        "fallback_used": False,
        "success": True,
        "errors": docs.get("errors") or [],
        "six_files": list(STANDARD_PACKET_FILES),
    }
