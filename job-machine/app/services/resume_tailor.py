from __future__ import annotations

from typing import Any

from app.config import get_settings
from app.services.filters import load_master_resume, load_profile
from app.services.truth_guard import scan_for_fabrication, truth_system_prompt


def _template_resume(job: dict[str, Any], projects: list[dict[str, Any]]) -> str:
    profile = load_profile()
    c = profile["candidate"]
    project_lines = []
    for p in projects[:4]:
        metrics = ", ".join(p.get("metrics", [])[:3])
        project_lines.append(f"- {p['name']}: {p['blurb']} ({metrics}) — {p['url']}")

    target = job.get("title", "AI Operations / Automation role")
    company = job.get("company", "the company")
    skills = " · ".join(profile["skills"][:12])
    tools = " · ".join(profile["tools"])

    return f"""# {c['full_name']}
{c['positioning']}
{c['location']} · Open to {c['open_to']}
{c['phone']} · {c['email']}
LinkedIn: {c['linkedin']}
Portfolio: {c['portfolio']}

## Target role alignment
Applying for: {target} at {company}
Available for remote AI Operations, Automation, Technical Support, and AI Implementation roles.

## Professional summary
Owner and AI Operations Specialist at {c['current_employer']}. Designs, tests, and documents AI-assisted workflows and no-code automation with n8n and Airtable. Hands-on delivery across GH-X automation (23 workflows / 8 stages), a 10-stage AI voice booking assistant, Harbor & Home product packaging, and LawOne AI platform foundations (in development). Emphasizes truthful implementation evidence — no invented scale metrics.

## Core skills
{skills}

## Experience
### {c['current_title']}
{c['current_employer']} — {c['location']} · Present
- Own and operate customer service and day-to-day business operations.
- Design, test, and improve AI-assisted booking workflows (qualification, pricing confirmation, appointments).
- Build and document no-code automation with n8n and Airtable.
- Run structured conversational testing: classify failures, root-cause, fix, retest, document.
- Use ChatGPT and Claude to prototype workflows and refine prompts.

## Selected projects matched to this role
{chr(10).join(project_lines)}

## Tools
{tools}

## Notes for reviewers
Education and certifications are listed only when verified. LawOne AI is in development and is not a finished commercial product.
"""


def _openai_resume(job: dict[str, Any], projects: list[dict[str, Any]]) -> str | None:
    settings = get_settings()
    if not settings.openai_api_key:
        return None
    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)
        master = load_master_resume()
        project_json = "\n".join(
            f"- {p['name']}: {p['blurb']} | {p['url']}" for p in projects
        )
        prompt = f"""Tailor a one-page markdown resume for this job using ONLY the master resume facts.

JOB TITLE: {job.get('title')}
COMPANY: {job.get('company')}
JOB DESCRIPTION:
{job.get('description','')[:6000]}

MATCHED PORTFOLIO PROJECTS TO EMPHASIZE:
{project_json}

MASTER RESUME:
{master[:12000]}

Output markdown only. Reorder and emphasize relevant bullets. Do not invent facts.
"""
        resp = client.chat.completions.create(
            model=settings.openai_model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": truth_system_prompt()},
                {"role": "user", "content": prompt},
            ],
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception:
        return None


def tailor_resume(job: dict[str, Any], projects: list[dict[str, Any]]) -> tuple[str, bool, list[str]]:
    ai_text = _openai_resume(job, projects)
    used_ai = bool(ai_text)
    text = ai_text or _template_resume(job, projects)
    warnings = scan_for_fabrication(text)
    if warnings and used_ai:
        # Fall back to safe template if AI drifted
        text = _template_resume(job, projects)
        warnings = scan_for_fabrication(text) + ["AI draft replaced by safe template due to truth warnings"]
        used_ai = False
    return text, used_ai, warnings
