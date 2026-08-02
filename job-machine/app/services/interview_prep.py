from __future__ import annotations

import json
from typing import Any

from app.config import get_settings
from app.services.filters import load_profile, normalize, text_blob
from app.services.pipeline_stages import PORTFOLIO_URL, TARGET_INTERVIEW_ROLES
from app.services.truth_guard import scan_for_fabrication, truth_system_prompt


def _role_family(title: str, blob: str) -> str:
    t = f"{title} {blob}"
    pairs = [
        ("ai operations", "AI Operations"),
        ("workflow automation", "Workflow Automation"),
        ("automation specialist", "Automation Specialist"),
        ("technical support", "Technical Support Engineer"),
        ("support engineer", "Technical Support Engineer"),
        ("solutions engineer", "Solutions Engineer"),
        ("customer success engineer", "Customer Success Engineer"),
        ("customer success", "Customer Success Engineer"),
        ("ai implementation", "AI Implementation"),
        ("implementation specialist", "AI Implementation"),
    ]
    for key, label in pairs:
        if key in t:
            return label
    return "AI Operations / Automation"


def _salary_block(job: dict[str, Any]) -> dict[str, Any]:
    text = (job.get("salary_text") or "").strip()
    smin = job.get("salary_min")
    smax = job.get("salary_max")
    if text:
        listed = text
    elif smin and smax:
        listed = f"${float(smin):,.0f} – ${float(smax):,.0f}"
    elif smin:
        listed = f"${float(smin):,.0f}+"
    elif smax:
        listed = f"Up to ${float(smax):,.0f}"
    else:
        listed = "Not listed on posting"
    return {
        "listed": listed,
        "research_notes": [
            "Confirm total compensation (base + bonus + equity) with the recruiter before negotiating.",
            "Ask for the budgeted range early: “What range is approved for this level?”",
            "For US remote ops/support/automation roles at growth companies, ranges often land mid-$60k to low-$100k depending on level — verify per company; do not invent a number.",
            "Leroy’s floor filter is $60,000+; only discuss numbers already on the posting or shared by the recruiter.",
        ],
        "talking_points": [
            "I am targeting remote AI Operations / Automation / Support roles at $60k+.",
            "I will share a number only after I understand the level and scope.",
            "I care about learning path, ownership of workflows, and clear success metrics as much as cash.",
        ],
    }


def _star_bank(projects: list[dict[str, Any]]) -> list[dict[str, str]]:
    """STAR stories grounded only in verified portfolio work."""
    by_id = {p.get("id"): p for p in projects}
    stories: list[dict[str, str]] = []

    ghx = by_id.get("ghx") or next((p for p in projects if "gh-x" in normalize(p.get("name", ""))), None)
    voice = by_id.get("voice") or next((p for p in projects if "voice" in normalize(p.get("name", ""))), None)
    qa = by_id.get("qa") or next((p for p in projects if "qa" in normalize(p.get("name", ""))), None)
    n8n = by_id.get("n8n") or next((p for p in projects if "n8n" in normalize(p.get("name", ""))), None)

    if ghx:
        stories.append(
            {
                "title": "Built a multi-stage automation pipeline (GH-X)",
                "situation": "I needed a repeatable way to move digital products through creation, packaging, and marketplace-ready stages without manual chaos.",
                "task": "Design and operate an automation system with clear stages, queues, and handoffs.",
                "action": f"I built the GH-X Automation System: {ghx.get('blurb')} Using n8n + Airtable, I defined stage gates, error handling, and documentation so each step was testable.",
                "result": "Documented evidence: "
                + ", ".join(ghx.get("metrics") or [])
                + f". Portfolio: {ghx.get('url')}",
            }
        )
    if voice:
        stories.append(
            {
                "title": "Improved AI booking reliability with structured QA",
                "situation": "An AI voice booking flow for a real service business was failing on edge cases (pricing confirmation, qualification, appointments).",
                "task": "Make the conversation safer and more consistent without inventing engineering seniority or fake call metrics.",
                "action": f"I designed a 10-stage booking conversation with prompt controls and confirmation checkpoints. {voice.get('blurb')} I classified failures, fixed prompts/rules, and retested.",
                "result": "Documented evidence: "
                + ", ".join(voice.get("metrics") or [])
                + f". Portfolio: {voice.get('url')}",
            }
        )
    if qa or n8n:
        p = qa or n8n
        stories.append(
            {
                "title": "Ran a disciplined QA / documentation loop",
                "situation": "Automation and conversational AI fail in messy real-world ways; undocumented fixes create regressions.",
                "task": "Create a repeatable quality process for AI workflows.",
                "action": f"{p.get('blurb')} I use a define → test → classify → root-cause → fix → retest → document loop so improvements stick.",
                "result": "Documented evidence: "
                + ", ".join(p.get("metrics") or [])
                + f". Portfolio: {p.get('url')}",
            }
        )

    if not stories:
        stories.append(
            {
                "title": "Owned AI operations work in a real business",
                "situation": "As Owner & AI Operations Specialist at Right Outside Auto Detailing LLC, I needed reliable customer and booking operations.",
                "task": "Use AI tools and no-code automation to improve day-to-day workflows truthfully.",
                "action": "I designed, tested, and documented AI-assisted workflows with ChatGPT/Claude, n8n, and Airtable — emphasizing verification over hype.",
                "result": f"Portfolio evidence lives at {PORTFOLIO_URL}. I do not invent revenue, call volume, or senior-engineer claims.",
            }
        )
    return stories


def _likely_questions(role: str) -> dict[str, list[str]]:
    common = [
        "Walk me through a workflow you built end-to-end.",
        "How do you decide what to automate vs. keep manual?",
        "Tell me about a time an AI workflow failed. What did you do?",
        "How do you document processes so others can run them?",
        "Why this company and this role?",
        "What does great customer/partner support look like to you?",
    ]
    technical = {
        "AI Operations": [
            "How do you evaluate prompt quality and prevent regressions?",
            "Describe your tooling stack for AI ops (n8n, Airtable, LLMs).",
            "How would you monitor an AI workflow in production for a small team?",
            "What’s your approach to handoff between AI and a human operator?",
        ],
        "Workflow Automation": [
            "Explain an n8n workflow with branching and error handling.",
            "How do you design queues and stage status in Airtable?",
            "What breaks first in brittle API automations — and how do you harden them?",
            "How do you version and document automation changes?",
        ],
        "Technical Support Engineer": [
            "How do you triage a customer issue you haven’t seen before?",
            "Explain a technical concept to a non-technical customer.",
            "How do you write clear bug reports for engineering?",
            "Describe your debugging process for an integration failure.",
        ],
        "Solutions Engineer": [
            "How would you run a discovery call for an automation use case?",
            "Walk through a demo agenda for a workflow product.",
            "How do you map customer pain to a feasible implementation?",
            "What’s your approach when a prospect asks for a custom integration?",
        ],
        "Customer Success Engineer": [
            "How do you turn a confused customer into a successful one?",
            "Describe onboarding for a technical product.",
            "How do you prioritize accounts when several need help?",
            "How do you feed product insights back from support conversations?",
        ],
        "AI Implementation": [
            "How do you scope an AI implementation so it ships?",
            "What does a safe rollout plan look like for a new AI workflow?",
            "How do you gather requirements without over-promising model capability?",
            "How do you measure implementation success beyond ‘it works’?",
        ],
        "Automation Specialist": [
            "Compare no-code vs. light-code for a given automation.",
            "How do you keep automations maintainable?",
            "Show how you’d design retry/backoff for a flaky API.",
            "How do you test automations before enabling them for customers?",
        ],
    }
    behavioral = [
        "Tell me about a time you owned a messy process and made it clearer.",
        "Describe a disagreement about priorities — how did you handle it?",
        "Give an example of learning a new tool quickly under pressure.",
        "Tell me about delivering under ambiguity with incomplete requirements.",
        "Describe how you handle feedback on something you built.",
    ]
    tech = technical.get(role) or technical["AI Operations"]
    return {
        "likely_interview_questions": common,
        "technical_questions": tech,
        "behavioral_questions": behavioral,
    }


def _company_research(job: dict[str, Any]) -> dict[str, Any]:
    company = job.get("company") or "the company"
    title = job.get("title") or "the role"
    return {
        "company": company,
        "role": title,
        "what_to_research_before_the_call": [
            f"Read the careers/about page for {company}: mission, products, recent launches.",
            "Skim LinkedIn posts from the hiring manager / team if named.",
            "Identify 1–2 products or workflows where AI ops, automation, or support quality clearly matter.",
            "Note whether the company is remote-first (GitLab, Automattic, Zapier-style) vs. remote-US with offices.",
            "Prepare one insight: “Here’s how my GH-X / voice booking / QA loop maps to your customers.”",
        ],
        "positioning_angle": (
            f"For {title} at {company}, lead with verified AI Operations / Workflow Automation evidence "
            f"(n8n, Airtable, prompt QA, support-style troubleshooting) and the live portfolio at {PORTFOLIO_URL}."
        ),
        "risks_to_avoid": [
            "Do not claim senior engineering, degrees, certifications, revenue, or call volume not in the portfolio.",
            "LawOne AI is in development — say that clearly if asked.",
            "Do not invent prior employers.",
        ],
    }


def _recruiter_cheat_sheet(job: dict[str, Any], projects: list[dict[str, Any]], why: str) -> dict[str, Any]:
    profile = load_profile()
    c = profile["candidate"]
    return {
        "elevator_30_seconds": (
            f"I’m {c['full_name']}, an AI Operations / Workflow Automation specialist based in {c['location']}. "
            f"I build and QA no-code AI workflows with n8n and Airtable — including a 23-workflow GH-X pipeline "
            f"and a 10-stage AI booking assistant — and I’m targeting remote {job.get('title')} roles."
        ),
        "why_this_role": why,
        "proof_links": [
            {"label": "Portfolio", "url": c["portfolio"]},
            {"label": "LinkedIn", "url": c["linkedin"]},
            *[{"label": p["name"], "url": p["url"]} for p in projects[:3]],
        ],
        "availability": "Remote US · ready for screening / first interview · applications require my explicit approval (no auto-apply).",
        "contact": {"email": c["email"], "phone": c["phone"]},
        "logistics_questions_for_recruiter": [
            "Is this role fully remote for US candidates?",
            "What is the interview process and expected timeline?",
            "What level / band is this role, and is the salary range posted accurate?",
            "Who would I partner with day-to-day (support, CS, product, ops)?",
        ],
    }


def _questions_to_ask(role: str) -> list[str]:
    return [
        "What does success look like in the first 30 / 60 / 90 days?",
        "Which workflows or customer problems are most painful right now?",
        "How does the team handle AI quality — who owns prompt/eval regressions?",
        "What’s the split between tooling (n8n/Airtable/etc.) and custom engineering?",
        f"For a {role}, how much time is customer-facing vs. building/improving systems?",
        "How do you document and hand off automations across the team?",
        "What does the interview process look like after this conversation?",
        "Is there anything in my background you want me to go deeper on?",
    ]


def build_interview_prep(
    job: dict[str, Any],
    projects: list[dict[str, Any]],
    *,
    why_match: str = "",
) -> dict[str, Any]:
    blob = text_blob(job)
    title = normalize(job.get("title", ""))
    role = _role_family(title, blob)
    questions = _likely_questions(role)
    stars = _star_bank(projects)
    prep = {
        "role_family": role,
        "optimized_for": TARGET_INTERVIEW_ROLES,
        "why_leroy_is_a_good_fit": why_match
        or "Verified remote AI Operations / automation evidence maps to this posting’s keywords and level.",
        "matched_portfolio_projects": [
            {"name": p.get("name"), "url": p.get("url"), "blurb": p.get("blurb"), "metrics": p.get("metrics")}
            for p in projects[:5]
        ],
        "portfolio_url": PORTFOLIO_URL,
        **questions,
        "star_answers": stars,
        "company_research": _company_research(job),
        "recruiter_cheat_sheet": _recruiter_cheat_sheet(job, projects, why_match),
        "salary_information": _salary_block(job),
        "questions_leroy_should_ask": _questions_to_ask(role),
        "truth_reminders": load_profile().get("truth_rules", []),
    }

    # Optional AI enrichment
    settings = get_settings()
    if settings.openai_api_key:
        enriched = _openai_enrich(job, projects, prep)
        if enriched:
            prep["ai_enrichment"] = enriched
            prep["used_ai"] = True
        else:
            prep["used_ai"] = False
    else:
        prep["used_ai"] = False

    # Truth scan on generated narrative fields
    narrative = json.dumps(
        {
            "stars": prep["star_answers"],
            "elevator": prep["recruiter_cheat_sheet"].get("elevator_30_seconds"),
            "why": prep["why_leroy_is_a_good_fit"],
        }
    )
    prep["truth_warnings"] = scan_for_fabrication(narrative)
    return prep


def _openai_enrich(job: dict[str, Any], projects: list[dict[str, Any]], base: dict[str, Any]) -> dict[str, Any] | None:
    settings = get_settings()
    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)
        project_lines = "\n".join(f"- {p['name']}: {p['blurb']}" for p in projects[:4])
        prompt = f"""You are preparing Leroy Garvin Jr for an interview.
Use ONLY verified facts. Do not invent employers, degrees, metrics, or seniority.

JOB: {job.get('title')} at {job.get('company')}
JD (excerpt):
{(job.get('description') or '')[:4000]}

PORTFOLIO:
{project_lines}

Return JSON with keys:
- extra_likely_questions (array of 5 strings)
- company_talking_points (array of 4 strings)
- closing_statement (1 short paragraph)
"""
        resp = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": truth_system_prompt()},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        text = resp.choices[0].message.content or ""
        # Best-effort JSON extract
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start : end + 1])
    except Exception:  # noqa: BLE001
        return None
    return None


def render_prep_markdown(prep: dict[str, Any], job: dict[str, Any]) -> str:
    lines = [
        f"# Interview Prep — {job.get('title')} @ {job.get('company')}",
        "",
        f"**Role family:** {prep.get('role_family')}",
        f"**Portfolio:** {prep.get('portfolio_url')}",
        "",
        "## Why Leroy is a good fit",
        prep.get("why_leroy_is_a_good_fit") or "",
        "",
        "## Matched portfolio projects",
    ]
    for p in prep.get("matched_portfolio_projects") or []:
        lines.append(f"- **{p.get('name')}** — {p.get('blurb')} ({p.get('url')})")
    lines += ["", "## Likely interview questions"]
    for q in prep.get("likely_interview_questions") or []:
        lines.append(f"- {q}")
    lines += ["", "## Technical questions"]
    for q in prep.get("technical_questions") or []:
        lines.append(f"- {q}")
    lines += ["", "## Behavioral questions"]
    for q in prep.get("behavioral_questions") or []:
        lines.append(f"- {q}")
    lines += ["", "## STAR answers (verified experience)"]
    for s in prep.get("star_answers") or []:
        lines.append(f"### {s.get('title')}")
        lines.append(f"- **S:** {s.get('situation')}")
        lines.append(f"- **T:** {s.get('task')}")
        lines.append(f"- **A:** {s.get('action')}")
        lines.append(f"- **R:** {s.get('result')}")
        lines.append("")
    cr = prep.get("company_research") or {}
    lines += ["## Company research", cr.get("positioning_angle", ""), ""]
    for item in cr.get("what_to_research_before_the_call") or []:
        lines.append(f"- {item}")
    cheat = prep.get("recruiter_cheat_sheet") or {}
    lines += ["", "## Recruiter cheat sheet", cheat.get("elevator_30_seconds", ""), ""]
    sal = prep.get("salary_information") or {}
    lines += ["## Salary information", f"Listed: {sal.get('listed')}", ""]
    for n in sal.get("research_notes") or []:
        lines.append(f"- {n}")
    lines += ["", "## Questions Leroy should ask"]
    for q in prep.get("questions_leroy_should_ask") or []:
        lines.append(f"- {q}")
    return "\n".join(lines)
