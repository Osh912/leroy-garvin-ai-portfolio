from __future__ import annotations

"""
Safe Application Autofill — localhost companion payloads and safety rules.
Never invents answers, never auto-submits, never fills sensitive self-ID fields.
"""

import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from sqlalchemy.orm import Session

from app.config import ROOT
from app.models import Application, Job
from app.services.filters import load_profile
from app.services.packet_store import _safe, packet_dir
from app.services.pipeline_stages import PORTFOLIO_URL, normalize_status
from app.services.truth_guard import scan_for_fabrication

ACTIVE_SESSION_PATH = ROOT / "data" / "autofill_active_session.json"
AUTOFILL_LOG_PATH = ROOT / "data" / "autofill_activity.log"

# Standard fields that may be filled after Confirm Autofill
SAFE_AUTOFILL_KEYS = [
    "first_name",
    "last_name",
    "email",
    "phone",
    "country",
    "city",
    "state",
    "zip_code",
    "linkedin",
    "portfolio",
    "github",
    "current_job_title",
]

# Never auto-answer these categories
SENSITIVE_QUESTION_PATTERNS = [
    r"\bdisability\b",
    r"\bdisabled\b",
    r"\bveteran\b",
    r"\bmilitary\b",
    r"\bgender\b",
    r"\bsex\b",
    r"\brace\b",
    r"\bethnic",
    r"\bhispanic\b",
    r"\blatin[oa]\b",
    r"\bsexual orientation\b",
    r"\bpronoun",
    r"\bcriminal\b",
    r"\bconviction\b",
    r"\bbackground check\b",
    r"\bsponsor",
    r"\bvisa\b",
    r"\bwork authorization\b",
    r"\bauthorized to work\b",
    r"\blegally (authorized|eligible)\b",
    r"\brequire sponsorship\b",
    r"\bsalary\b",
    r"\bcompensation\b",
    r"\bdesired pay\b",
    r"\bexpected (pay|salary|comp)",
    r"\beeo\b",
    r"\bequal opportunity\b",
    r"\bvoluntary self",
    r"\bprotected veteran\b",
    r"\bdemograph",
]

# Draftable custom questions (still require Leroy approval)
DRAFTABLE_PATTERNS = [
    (r"why (are you )?interested", "interest"),
    (r"why (this|our) (role|position|job|company|team)", "interest"),
    (r"what (attracts|interests) you", "interest"),
    (r"relevant experience", "experience"),
    (r"tell us about (yourself|your experience)", "experience"),
    (r"describe .+ experience", "experience"),
    (r"cover letter", "cover"),
    (r"additional information", "additional"),
    (r"anything else", "additional"),
    (r"start date", "start_date"),
    (r"when can you start", "start_date"),
    (r"earliest start", "start_date"),
]

PLATFORM_HOST_RULES: list[tuple[str, list[str]]] = [
    ("greenhouse", ["greenhouse.io", "boards.greenhouse.io", "job-boards.greenhouse.io"]),
    ("lever", ["lever.co", "jobs.lever.co"]),
    ("ashby", ["ashbyhq.com", "jobs.ashbyhq.com"]),
    ("smartrecruiters", ["smartrecruiters.com", "jobs.smartrecruiters.com"]),
    ("workday", ["myworkdayjobs.com", "workday.com"]),
    ("indeed", ["indeed.com"]),
    ("linkedin", ["linkedin.com"]),
]


def _candidate() -> dict[str, Any]:
    profile = load_profile()
    return profile.get("candidate") or {}


def _append_log(event: str, details: dict[str, Any]) -> None:
    AUTOFILL_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(
        {"ts": datetime.utcnow().isoformat() + "Z", "event": event, **details},
        ensure_ascii=False,
    )
    with AUTOFILL_LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def detect_platform(url: str) -> str:
    host = (urlparse(url or "").hostname or "").lower()
    path = (urlparse(url or "").path or "").lower()
    for name, needles in PLATFORM_HOST_RULES:
        if any(n in host for n in needles):
            return name
    if "linkedin.com" in host and ("/jobs/" in path or "externalApply" in (url or "")):
        return "linkedin"
    if host:
        return "generic"
    return "unknown"


def is_sensitive_question(text: str) -> bool:
    t = (text or "").lower()
    return any(re.search(p, t) for p in SENSITIVE_QUESTION_PATTERNS)


def draftable_kind(text: str) -> str | None:
    if is_sensitive_question(text):
        return None
    t = (text or "").lower()
    for pattern, kind in DRAFTABLE_PATTERNS:
        if re.search(pattern, t):
            return kind
    return None


def verified_autofill_fields() -> dict[str, Any]:
    """Only return verified profile values. Null/empty means do not fill."""
    c = _candidate()
    fields = {
        "first_name": c.get("first_name") or (c.get("full_name") or "").split(" ")[0],
        "last_name": c.get("last_name")
        or " ".join((c.get("full_name") or "").split(" ")[1:])
        or None,
        "email": c.get("email"),
        "phone": c.get("phone"),
        "country": c.get("country") or "United States",
        "city": c.get("city"),
        "state": c.get("state") or c.get("state_full"),
        "zip_code": c.get("zip_code"),  # null unless verified — never invent
        "linkedin": c.get("linkedin"),
        "portfolio": c.get("portfolio") or PORTFOLIO_URL,
        "github": c.get("github"),  # only if present in profile
        "current_job_title": c.get("current_title"),
    }
    # Strip empties / explicit nulls for fill list; keep keys for preview transparency
    return {k: (v if v not in ("", None) else None) for k, v in fields.items()}


def _meta(row: Application) -> dict[str, Any]:
    try:
        data = json.loads(getattr(row, "analytics_json", None) or "{}")
    except json.JSONDecodeError:
        data = {}
    return data if isinstance(data, dict) else {}


def _save_meta(row: Application, meta: dict[str, Any]) -> None:
    row.analytics_json = json.dumps(meta)


def ensure_application_files(row: Application, job: Job | None) -> dict[str, Any]:
    """Write job-specific resume/cover files locally. Verify company/role in filenames."""
    company = row.company
    title = row.position
    folder = packet_dir(row.job_id or row.id, company, title)
    resume_path = folder / f"{_safe(company)}_{_safe(title)}_resume.md"
    cover_path = folder / f"{_safe(company)}_{_safe(title)}_cover.md"
    resume_txt = folder / f"{_safe(company)}_{_safe(title)}_resume.txt"
    cover_txt = folder / f"{_safe(company)}_{_safe(title)}_cover.txt"

    resume = row.tailored_resume or ""
    cover = row.cover_letter or ""
    if resume:
        resume_path.write_text(resume, encoding="utf-8")
        resume_txt.write_text(resume, encoding="utf-8")
    if cover:
        cover_path.write_text(cover, encoding="utf-8")
        cover_txt.write_text(cover, encoding="utf-8")

    # Optional simple PDFs when reportlab available
    resume_pdf = folder / f"{_safe(company)}_{_safe(title)}_resume.pdf"
    cover_pdf = folder / f"{_safe(company)}_{_safe(title)}_cover.pdf"
    pdf_ok = False
    if resume or cover:
        try:
            pdf_ok = _write_text_pdf(resume_pdf, f"Resume — {title} @ {company}", resume)
            _write_text_pdf(cover_pdf, f"Cover Letter — {title} @ {company}", cover)
        except Exception:  # noqa: BLE001
            pdf_ok = False

    return {
        "company": company,
        "role": title,
        "job_id": row.job_id,
        "application_id": row.id,
        "resume_version": _meta(row).get("resume_version") or "tailored",
        "cover_version": _meta(row).get("cover_version") or "tailored",
        "resume_md": str(resume_path) if resume_path.exists() else None,
        "cover_md": str(cover_path) if cover_path.exists() else None,
        "resume_txt": str(resume_txt) if resume_txt.exists() else None,
        "cover_txt": str(cover_txt) if cover_txt.exists() else None,
        "resume_pdf": str(resume_pdf) if pdf_ok and resume_pdf.exists() else None,
        "cover_pdf": str(cover_pdf) if cover_pdf.exists() and pdf_ok else None,
        "download_resume_url": f"/api/autofill/applications/{row.id}/files/resume",
        "download_cover_url": f"/api/autofill/applications/{row.id}/files/cover",
        "verify_token": f"{row.id}:{_safe(company)}:{_safe(title)}",
    }


def _write_text_pdf(path: Path, title: str, body: str) -> bool:
    if not body.strip():
        return False
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=letter)
    width, height = letter
    y = height - 50
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, title[:90])
    y -= 24
    c.setFont("Helvetica", 9)
    for line in body.splitlines() or [""]:
        for chunk in _wrap(line, 95):
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 9)
                y = height - 50
            c.drawString(50, y, chunk[:120])
            y -= 12
    c.save()
    return path.exists()


def _wrap(text: str, width: int) -> list[str]:
    if not text:
        return [""]
    words = text.split()
    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        trial = " ".join(cur + [w])
        if len(trial) > width:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(" ".join(cur))
    return lines or [""]


def safety_check(row: Application, job: Job | None, files: dict[str, Any]) -> dict[str, Any]:
    fields = verified_autofill_fields()
    warnings = scan_for_fabrication((row.tailored_resume or "") + "\n" + (row.cover_letter or ""))
    items = {
        "correct_company": bool(row.company) and (not job or row.company == job.company),
        "correct_job_title": bool(row.position) and (not job or row.position == job.title),
        "correct_resume_version": bool(row.tailored_resume and files.get("resume_txt")),
        "correct_cover_letter_version": bool(row.cover_letter and files.get("cover_txt")),
        "portfolio_url_included": bool(fields.get("portfolio")),
        "linkedin_url_included": bool(fields.get("linkedin")),
        "contact_information_verified": bool(fields.get("email") and fields.get("phone")),
        "required_questions_reviewed": False,  # Leroy must confirm in extension
        "no_unsupported_claims_detected": len(warnings) == 0,
    }
    return {
        "items": items,
        "truth_warnings": warnings,
        "ready_for_manual_submit": all(
            items[k]
            for k in items
            if k not in {"required_questions_reviewed"}  # always manual in UI
        ),
        "company": row.company,
        "job_title": row.position,
        "resume_version": files.get("resume_version"),
        "cover_version": files.get("cover_version"),
    }


def build_autofill_payload(row: Application, db: Session) -> dict[str, Any]:
    job = db.get(Job, row.job_id) if row.job_id else None
    url = (job.url if job else "") or ""
    platform = detect_platform(url)
    fields = verified_autofill_fields()
    files = ensure_application_files(row, job)
    check = safety_check(row, job, files)
    fillable = {k: fields[k] for k in SAFE_AUTOFILL_KEYS if fields.get(k)}
    manual_only = [k for k in SAFE_AUTOFILL_KEYS if not fields.get(k)]
    meta = _meta(row)

    return {
        "mode": "safe_autofill",
        "auto_submit": False,
        "requires_confirm_autofill": True,
        "captcha_bypass": False,
        "fabricated": False,
        "local_only": True,
        "application_id": row.id,
        "job_id": row.job_id,
        "company": row.company,
        "position": row.position,
        "application_url": url,
        "platform": platform,
        "fields": fields,
        "fillable_fields": fillable,
        "manual_or_missing_fields": manual_only,
        "files": files,
        "safety_check": check,
        "sensitive_policy": {
            "never_auto_answer": [
                "disability",
                "veteran",
                "demographic/EEO",
                "sponsorship / work authorization",
                "criminal history",
                "salary / compensation",
                "custom screening without review",
            ],
            "draft_requires_approval": True,
        },
        "resume_version": files.get("resume_version"),
        "cover_version": files.get("cover_version"),
        "recruiter_summary": meta.get("recruiter_summary") or "",
        "portfolio_refs": json.loads(row.portfolio_refs or "[]"),
        "never_click_submit": True,
        "api_base": "http://127.0.0.1:8787",
    }


def set_active_session(payload: dict[str, Any]) -> None:
    ACTIVE_SESSION_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        **payload,
        "activated_at": datetime.utcnow().isoformat() + "Z",
        "status": "awaiting_confirm_autofill",
    }
    ACTIVE_SESSION_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    _append_log("session_activated", {"application_id": payload.get("application_id"), "platform": payload.get("platform")})


def get_active_session() -> dict[str, Any] | None:
    if not ACTIVE_SESSION_PATH.exists():
        return None
    try:
        return json.loads(ACTIVE_SESSION_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def clear_active_session() -> None:
    if ACTIVE_SESSION_PATH.exists():
        ACTIVE_SESSION_PATH.unlink()


def open_application_session(app_id: int, db: Session) -> dict[str, Any]:
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    if not (row.tailored_resume and row.cover_letter):
        # Encourage prepare first, but still allow open if materials partial
        pass
    payload = build_autofill_payload(row, db)
    if not payload.get("application_url"):
        raise ValueError("No application URL on this job. Import or search a job with a posting URL first.")
    set_active_session(payload)
    meta = _meta(row)
    meta["autofill"] = {
        **(meta.get("autofill") or {}),
        "last_opened_at": datetime.utcnow().isoformat() + "Z",
        "platform": payload["platform"],
        "application_url": payload["application_url"],
    }
    _save_meta(row, meta)
    db.add(row)
    db.commit()
    return payload


def suggest_answer(app_id: int, question: str, db: Session) -> dict[str, Any]:
    """Suggested draft only — never auto-submitted. Sensitive questions stay unanswered."""
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    q = (question or "").strip()
    if not q:
        raise ValueError("Question text required")

    if is_sensitive_question(q):
        return {
            "question": q,
            "sensitive": True,
            "suggested_answer": None,
            "label": "Manual selection required",
            "source_facts": [],
            "requires_review": True,
            "auto_fill": False,
            "note": "Sensitive / self-identification / legal / salary / sponsorship questions are never auto-answered.",
        }

    kind = draftable_kind(q)
    c = _candidate()
    projects = json.loads(row.portfolio_refs or "[]")
    project_names = [p.get("name") for p in projects if p.get("name")]
    source_facts = [
        f"Role: {row.position} @ {row.company}",
        f"Positioning: {c.get('positioning')}",
        f"Current title: {c.get('current_title')}",
        f"Portfolio: {c.get('portfolio') or PORTFOLIO_URL}",
    ]
    if project_names:
        source_facts.append("Matched projects: " + ", ".join(project_names[:4]))

    draft = None
    if kind == "interest":
        draft = (
            f"I'm interested in the {row.position} role at {row.company} because it aligns with my focus on "
            f"{c.get('positioning')}. I currently work as {c.get('current_title')} and build practical AI/workflow "
            f"automation systems. Relevant portfolio work includes: {', '.join(project_names[:3]) or 'my public portfolio'}. "
            f"Portfolio: {c.get('portfolio') or PORTFOLIO_URL}."
        )
    elif kind == "experience":
        draft = (
            f"In my current role as {c.get('current_title')}, I design and operate AI/workflow automation processes "
            f"(tools such as n8n, Airtable, and LLM assistants). For {row.company}, I can apply the same approach to "
            f"reliable support and automation operations. Evidence: {', '.join(project_names[:3]) or (c.get('portfolio') or PORTFOLIO_URL)}."
        )
    elif kind == "cover":
        draft = (row.cover_letter or "")[:2000] or None
        if draft:
            source_facts.append("Source: tailored cover letter stored on this application")
    elif kind == "additional":
        draft = (
            f"Additional materials: Portfolio {c.get('portfolio') or PORTFOLIO_URL}; "
            f"LinkedIn {c.get('linkedin')}. Happy to share job-specific resume/cover for {row.company}."
        )
    elif kind == "start_date":
        draft = None  # leave blank — Leroy must choose; don't invent availability
        return {
            "question": q,
            "sensitive": False,
            "suggested_answer": None,
            "label": "Suggested Answer unavailable — choose your own start date",
            "source_facts": source_facts,
            "requires_review": True,
            "auto_fill": False,
            "note": "Start dates are never invented.",
        }
    else:
        return {
            "question": q,
            "sensitive": False,
            "suggested_answer": None,
            "label": "No draft — manual answer required",
            "source_facts": source_facts,
            "requires_review": True,
            "auto_fill": False,
            "note": "No safe draft template for this question. Answer manually.",
        }

    warnings = scan_for_fabrication(draft or "")
    return {
        "question": q,
        "sensitive": False,
        "suggested_answer": draft,
        "label": "Suggested Answer",
        "source_facts": source_facts,
        "truth_warnings": warnings,
        "requires_review": True,
        "auto_fill": False,
        "approval_required": True,
        "note": "Review, edit, and approve before pasting. Nothing is submitted automatically.",
    }


def mark_submitted(
    app_id: int,
    db: Session,
    *,
    application_url: str | None = None,
    platform: str | None = None,
    notes: str | None = None,
    resume_version: str | None = None,
    cover_version: str | None = None,
) -> dict[str, Any]:
    row = db.get(Application, app_id)
    if not row:
        raise ValueError("Application not found")
    job = db.get(Job, row.job_id) if row.job_id else None
    url = application_url or (job.url if job else "") or ""
    plat = platform or detect_platform(url)
    now = datetime.utcnow()
    meta = _meta(row)
    files = ensure_application_files(row, job)
    submission = {
        "company": row.company,
        "role": row.position,
        "application_url": url,
        "submitted_at": now.isoformat() + "Z",
        "resume_version": resume_version or files.get("resume_version"),
        "cover_version": cover_version or files.get("cover_version"),
        "platform": plat,
        "follow_up_date": (date.today() + timedelta(days=5)).isoformat(),
        "notes": notes or "Manually submitted by Leroy. Autofill companion did not click Submit.",
        "marked_via": "safe_autofill",
    }
    meta["submission"] = submission
    meta.setdefault("autofill", {})
    meta["autofill"]["marked_submitted_at"] = submission["submitted_at"]
    _save_meta(row, meta)

    row.status = "applied"
    row.date_applied = date.today()
    row.follow_up_date = date.today() + timedelta(days=5)
    stamp = f"\n[{now.isoformat()}Z] Marked Submitted via Safe Autofill ({plat}). URL: {url}"
    row.notes = ((row.notes or "").rstrip() + stamp).strip()
    if job:
        job.status = "applied"
    db.add(row)
    db.commit()
    db.refresh(row)
    _append_log("marked_submitted", {"application_id": app_id, "platform": plat, "company": row.company})
    clear_active_session()
    return {
        "application_id": row.id,
        "status": row.status,
        "submission": submission,
        "auto_submit": False,
        "message": "Recorded as submitted. Follow-up date set (+5 days).",
    }


def verify_file_belongs_to_application(app_id: int, filename: str, db: Session) -> bool:
    row = db.get(Application, app_id)
    if not row:
        return False
    company_token = _safe(row.company).lower()
    role_token = _safe(row.position).lower()
    name = (filename or "").lower()
    return company_token in name and role_token in name


def classify_detected_fields(detected: list[dict[str, Any]]) -> dict[str, Any]:
    """Server-side classification for extension preview."""
    fields = verified_autofill_fields()
    autofill: list[dict[str, Any]] = []
    manual: list[dict[str, Any]] = []
    sensitive: list[dict[str, Any]] = []
    draftable: list[dict[str, Any]] = []

    for item in detected:
        label = item.get("label") or item.get("name") or item.get("id") or ""
        key = (item.get("mapped_key") or "").strip()
        if is_sensitive_question(label) or is_sensitive_question(key):
            sensitive.append({**item, "action": "manual_only", "reason": "sensitive_question"})
            continue
        if key in fields and fields.get(key):
            autofill.append(
                {
                    **item,
                    "action": "autofill_after_confirm",
                    "value": fields[key],
                }
            )
            continue
        kind = draftable_kind(label)
        if kind:
            draftable.append({**item, "action": "suggested_draft", "draft_kind": kind})
            continue
        manual.append({**item, "action": "manual_review"})

    return {
        "autofill_candidates": autofill,
        "manual_review": manual,
        "sensitive_manual": sensitive,
        "draftable": draftable,
        "submit_buttons_will_not_be_clicked": True,
    }
