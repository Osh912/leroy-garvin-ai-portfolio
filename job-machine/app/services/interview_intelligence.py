from __future__ import annotations

"""
Interview Intelligence — pre-interview brief from verified profile + job text only.
Never invents company finances, news, competitors, education, or experience.
"""

import json
import re
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models import Application, Job
from app.services.filters import load_profile, match_reason, normalize
from app.services.interview_prep import build_interview_prep, render_prep_markdown
from app.services.pipeline_stages import PORTFOLIO_URL
from app.services.portfolio_matcher import match_portfolio
from app.services.truth_guard import scan_for_fabrication


def generate_interview_intelligence(app_id: int | None, job_id: int | None, db: Session) -> dict[str, Any]:
    row: Application | None = db.get(Application, app_id) if app_id else None
    job: Job | None = None
    if job_id:
        job = db.get(Job, job_id)
    elif row:
        job = db.get(Job, row.job_id) if row.job_id else None
    if not job and not row:
        raise ValueError("Provide application_id or job_id")

    company = (job.company if job else None) or (row.company if row else "")
    title = (job.title if job else None) or (row.position if row else "")
    description = (job.description if job else "") or ""
    salary_text = (job.salary_text if job else None) or (row.salary if row else "") or ""

    job_dict = {
        "title": title,
        "company": company,
        "location": (job.location if job else None) or (row.location if row else "Remote"),
        "description": description,
        "salary_text": salary_text,
        "salary_min": job.salary_min if job else None,
        "salary_max": job.salary_max if job else None,
        "tags": job.tags if job else "",
        "source": job.source if job else "",
    }
    projects = match_portfolio(job_dict)
    why = match_reason(job_dict, projects)
    prep = build_interview_prep(job_dict, projects, why_match=why)
    candidate = (load_profile().get("candidate") or {})

    research = _company_research_from_posting(company, description, job_dict)
    elevator = _elevator_pitch(candidate, title, company, projects)
    tech_topics = _technical_topics(description, job_dict.get("tags") or "")
    salary_notes = prep.get("salary_negotiation") or {
        "listed": salary_text or "Not listed on posting",
        "research_notes": [
            "Only discuss numbers listed on the posting or shared by the recruiter.",
            "Do not invent a competing offer or equity package.",
        ],
    }

    star = prep.get("star_answers") or []
    questions = prep.get("questions_leroy_should_ask") or []
    pitch_warnings = scan_for_fabrication(elevator)
    star_text = json.dumps(star)
    star_warnings = scan_for_fabrication(star_text)

    brief = {
        "mode": "interview_intelligence",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "fabricated": False,
        "auto_apply": False,
        "auto_email": False,
        "approval_required": True,
        "application_id": row.id if row else None,
        "job_id": job.id if job else None,
        "company": company,
        "position": title,
        "company_research": research["summary"],
        "financial_overview": research["financial_overview"],
        "products": research["products"],
        "competitors": research["competitors"],
        "company_culture": research["culture"],
        "latest_news": research["latest_news"],
        "star_answers": star,
        "questions_to_ask_interviewer": questions,
        "technical_topics_likely": tech_topics,
        "elevator_pitch_30s": elevator,
        "salary_negotiation_notes": salary_notes,
        "why_match": why,
        "matched_projects": projects,
        "prep_markdown": render_prep_markdown(prep, {"title": title, "company": company}),
        "truth_warnings": list(dict.fromkeys(pitch_warnings + star_warnings + research["warnings"])),
        "data_sources": [
            "Job posting text (local DB)",
            "Verified profile.json",
            "Verified portfolio_projects.json",
            "Existing interview_prep STAR bank (real projects only)",
        ],
        "notes": [
            "Financials, competitors, and news are only filled when extractable from the posting — otherwise marked unavailable.",
            "Never invent experience, education, or certifications.",
            "Review before the interview; nothing is sent automatically.",
        ],
    }

    if row:
        try:
            meta = json.loads(row.analytics_json or "{}")
        except json.JSONDecodeError:
            meta = {}
        meta["interview_intelligence"] = {
            "generated_at": brief["generated_at"],
            "company": company,
            "position": title,
        }
        row.analytics_json = json.dumps(meta)
        row.interview_prep = json.dumps(prep)
        db.add(row)
        db.commit()

    return brief


def _company_research_from_posting(company: str, description: str, job: dict[str, Any]) -> dict[str, Any]:
    blob = description or ""
    products = _extract_products(blob)
    culture = _extract_culture(blob)
    competitors = _extract_competitors(blob)
    financial = _extract_financial(blob)
    news = _extract_news_mentions(blob)
    warnings: list[str] = []

    if not financial["available"]:
        warnings.append("No verified financial figures in posting — financial overview left unavailable.")
    if not competitors:
        warnings.append("No competitors named in posting — do not invent a competitor list.")
    if not news["items"]:
        warnings.append("No dated news items in posting — latest news left unavailable (research manually).")

    summary = (
        f"{company} — research compiled from the job posting only. "
        f"Role: {job.get('title')}. Location: {job.get('location')}. "
        "External web claims are not fetched or invented by Job Machine."
    )
    return {
        "summary": summary,
        "financial_overview": financial,
        "products": products or ["Not specified in posting — research on company site before interview."],
        "competitors": competitors
        or ["Unavailable from posting — do not fabricate competitor names."],
        "culture": culture
        or ["Culture cues not explicit in posting — ask the interviewer about team rituals and success metrics."],
        "latest_news": news,
        "warnings": warnings,
    }


def _extract_products(text: str) -> list[str]:
    products = []
    # Capture "our product X" / "platform" phrases lightly
    for m in re.finditer(r"(?:our|the)\s+([A-Z][\w]+(?:\s+[A-Z][\w]+){0,3})\s+(?:platform|product|suite|API)", text):
        products.append(m.group(0).strip())
    # Tools listed after common headings
    for m in re.finditer(r"(?:tech stack|tools?|technologies)[:\s]+([^\n]{10,160})", text, re.I):
        products.append("Stack/tools mentioned: " + m.group(1).strip())
    return list(dict.fromkeys(products))[:8]


def _extract_culture(text: str) -> list[str]:
    cues = []
    patterns = [
        r"remote[- ]first[^\n.]{0,80}",
        r"fully remote[^\n.]{0,80}",
        r"inclusive[^\n.]{0,80}",
        r"collaborat(?:ive|ion)[^\n.]{0,80}",
        r"async(?:hronous)?[^\n.]{0,80}",
        r"customer[- ]obsessed[^\n.]{0,80}",
    ]
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            cues.append(m.group(0).strip())
    return list(dict.fromkeys(cues))[:8]


def _extract_competitors(text: str) -> list[str]:
    m = re.search(r"competitors?(?:\s+include|\s*:)\s*([^\n.]{5,160})", text, re.I)
    if not m:
        return []
    parts = re.split(r",|/| and ", m.group(1))
    return [p.strip() for p in parts if p.strip()][:8]


def _extract_financial(text: str) -> dict[str, Any]:
    # Only surface figures explicitly in posting (funding, ARR mentions)
    figures = re.findall(
        r"((?:\$\d+(?:\.\d+)?\s*(?:M|B|million|billion)|Series\s+[A-D]|ARR|revenue)[^\n.]{0,60})",
        text,
        re.I,
    )
    if not figures:
        return {
            "available": False,
            "figures": [],
            "note": "No financial figures found in the job posting. Do not invent valuation/revenue.",
        }
    return {
        "available": True,
        "figures": [f.strip() for f in figures[:6]],
        "note": "Extracted only from posting text — verify independently before citing in interview.",
    }


def _extract_news_mentions(text: str) -> dict[str, Any]:
    items = []
    for m in re.finditer(r"(in\s+\d{4}[^\n.]{0,100}|recently[^\n.]{0,100}|announced[^\n.]{0,100})", text, re.I):
        items.append(m.group(0).strip())
    return {
        "available": bool(items),
        "items": items[:5],
        "note": "Only phrases from the posting. For real-time news, review the company site manually.",
    }


def _technical_topics(description: str, tags: str) -> list[str]:
    blob = normalize(f"{description} {tags}")
    candidates = [
        ("n8n", "n8n / workflow automation"),
        ("airtable", "Airtable / no-code ops"),
        ("python", "Python scripting"),
        ("sql", "SQL / data lookups"),
        ("api", "APIs / integrations"),
        ("zendesk", "Zendesk / support tooling"),
        ("salesforce", "Salesforce"),
        ("prompt", "Prompt engineering / LLM QA"),
        ("rag", "RAG / knowledge retrieval"),
        ("troubleshooting", "Troubleshooting / RCA"),
        ("documentation", "Process documentation"),
        ("customer", "Customer communication"),
    ]
    found = [label for key, label in candidates if key in blob]
    return found or ["Role fundamentals from the posting — review requirements line by line."]


def _elevator_pitch(candidate: dict[str, Any], title: str, company: str, projects: list[dict[str, Any]]) -> str:
    name = candidate.get("full_name") or "Leroy Garvin Jr"
    positioning = candidate.get("positioning") or "AI Automation | AI Operations | Workflow Automation"
    current = candidate.get("current_title") or "AI Operations Specialist"
    portfolio = candidate.get("portfolio") or PORTFOLIO_URL
    proj = ", ".join(p.get("name") for p in projects[:2] if p.get("name")) or "my public portfolio projects"
    return (
        f"I'm {name}, focused on {positioning}. "
        f"As {current}, I design practical AI and workflow automations with clear stages and QA. "
        f"For the {title} role at {company}, I can bring evidence from {proj}. "
        f"Portfolio: {portfolio}."
    )
