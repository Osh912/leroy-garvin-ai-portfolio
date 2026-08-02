from __future__ import annotations

from typing import Any

from app.config import get_settings
from app.services.filters import load_profile
from app.services.truth_guard import scan_for_fabrication, truth_system_prompt


def _template_cover(job: dict[str, Any], projects: list[dict[str, Any]]) -> str:
    profile = load_profile()
    c = profile["candidate"]
    title = job.get("title", "the role")
    company = job.get("company", "your team")
    top = projects[:3]
    bullets = "\n".join(
        f"- {p['name']}: {p['blurb']}" for p in top
    )
    links = "\n".join(f"- {p['name']}: {p['url']}" for p in top)

    return f"""Dear Hiring Team at {company},

I am applying for the {title} role. I help companies design, test, and run AI-assisted business workflows — with honest, evidence-backed implementation experience.

As Owner & AI Operations Specialist at {c['current_employer']}, I build practical systems using n8n, Airtable, prompt engineering, and structured QA. Relevant proof points for this role:

{bullets}

I am available for remote AI Operations, Automation, Technical Support, and AI Implementation work. I do not invent metrics or overstate engineering seniority — my portfolio shows verified project evidence.

Portfolio: {c['portfolio']}
Selected project links:
{links}

Thank you for your time. I would welcome a conversation about how I can support your team.

Sincerely,
{c['full_name']}
{c['phone']} · {c['email']}
{c['linkedin']}
"""


def _openai_cover(job: dict[str, Any], projects: list[dict[str, Any]]) -> str | None:
    settings = get_settings()
    if not settings.openai_api_key:
        return None
    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)
        profile = load_profile()
        c = profile["candidate"]
        project_block = "\n".join(f"- {p['name']}: {p['blurb']} ({p['url']})" for p in projects)
        prompt = f"""Write a unique, concise cover letter (250–350 words) for Leroy Garvin Jr.

CANDIDATE FACTS:
- Name: {c['full_name']}
- Title: {c['current_title']} at {c['current_employer']}
- Positioning: {c['positioning']}
- Portfolio: {c['portfolio']}
- Location: {c['location']}, open to remote

JOB:
- Title: {job.get('title')}
- Company: {job.get('company')}
- Description: {job.get('description','')[:5000]}

PORTFOLIO PROJECTS TO REFERENCE:
{project_block}

Tone: professional, direct, confident, truthful. No fluff. No invented achievements.
"""
        resp = client.chat.completions.create(
            model=settings.openai_model,
            temperature=0.4,
            messages=[
                {"role": "system", "content": truth_system_prompt()},
                {"role": "user", "content": prompt},
            ],
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception:
        return None


def generate_cover_letter(job: dict[str, Any], projects: list[dict[str, Any]]) -> tuple[str, bool, list[str]]:
    ai_text = _openai_cover(job, projects)
    used_ai = bool(ai_text)
    text = ai_text or _template_cover(job, projects)
    warnings = scan_for_fabrication(text)
    if warnings and used_ai:
        text = _template_cover(job, projects)
        warnings = scan_for_fabrication(text) + ["AI draft replaced by safe template due to truth warnings"]
        used_ai = False
    return text, used_ai, warnings
