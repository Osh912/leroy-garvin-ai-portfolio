from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from app.config import ROOT
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
    """Persist resume, cover, prep, and meta under data/interview_packets/."""
    profile = load_profile()
    folder = packet_dir(job_id, company, title)
    (folder / "resume.md").write_text(resume, encoding="utf-8")
    (folder / "cover_letter.md").write_text(cover, encoding="utf-8")
    (folder / "interview_prep.json").write_text(json.dumps(prep, indent=2), encoding="utf-8")

    from app.services.interview_prep import render_prep_markdown

    prep_md = render_prep_markdown(prep, {"title": title, "company": company})
    (folder / "interview_prep.md").write_text(prep_md, encoding="utf-8")

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
        "paths": {
            "resume": str(folder / "resume.md"),
            "cover_letter": str(folder / "cover_letter.md"),
            "interview_prep_json": str(folder / "interview_prep.json"),
            "interview_prep_md": str(folder / "interview_prep.md"),
        },
    }
    (folder / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta["paths"]


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
) -> dict[str, str]:
    """Return text payloads for one-click export (client downloads)."""
    return {
        "resume_filename": f"{_safe(company)}_{_safe(title)}_resume.md",
        "cover_filename": f"{_safe(company)}_{_safe(title)}_cover.md",
        "resume": resume,
        "cover_letter": cover,
        "portfolio_url": portfolio_url or PORTFOLIO_URL,
        "export_note": "Applications require Leroy's approval — never auto-submitted.",
    }
