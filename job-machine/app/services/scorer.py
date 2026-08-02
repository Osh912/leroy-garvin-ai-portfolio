from __future__ import annotations

"""
Career Agent 2.0 — Transparent Match Score v2.

Weights (always explainable; never invents interview odds):
  35% Skill match
  25% Interview readiness (signals from JD↔profile fit — NOT a predicted interview %)
  15% Remote verification
  10% Salary fit
   5% Career growth signals
   5% Resume strength
   5% Portfolio match

interview_probability remains null — never fabricated.
"""

from typing import Any

from app.services.filters import (
    LEVEL_KEYWORDS,
    PRIORITY_TITLE_TERMS,
    ROLE_KEYWORDS,
    load_master_resume,
    load_profile,
    normalize,
    priority_title_hit,
    requires_five_plus_years,
    salary_mid,
    text_blob,
    verify_remote,
)
from app.services.portfolio_matcher import match_portfolio

W_SKILL = 0.35
W_INTERVIEW_READINESS = 0.25
W_REMOTE = 0.15
W_SALARY = 0.10
W_CAREER_GROWTH = 0.05
W_RESUME = 0.05
W_PORTFOLIO = 0.05

SKILL_TOOLS = [
    "n8n",
    "airtable",
    "openai",
    "python",
    "prompt",
    "automation",
    "workflow",
    "support",
    "implementation",
    "qa",
    "operations",
    "zapier",
    "make.com",
    "llm",
    "chatgpt",
    "claude",
]


def _skill_score(job: dict[str, Any], blob: str, title: str) -> tuple[float, list[str]]:
    hits = [k for k in ROLE_KEYWORDS if k in blob]
    tools = [t for t in SKILL_TOOLS if t in blob]
    score = min(70.0, len(hits) * 8.0 + len(tools) * 5.0)
    evidence: list[str] = []
    if priority_title_hit(job):
        score += 18
        evidence.append("Title matches a target role family")
    elif any(t in title for t in PRIORITY_TITLE_TERMS):
        score += 12
        evidence.append("Title contains target role keywords")
    if any(k in title for k in LEVEL_KEYWORDS):
        score += 8
    if tools:
        evidence.append("JD tools overlap: " + ", ".join(tools[:6]))
    if hits:
        evidence.append("Role keywords: " + ", ".join(hits[:5]))
    return max(0.0, min(100.0, score)), evidence


def _resume_score(job: dict[str, Any], blob: str) -> tuple[float, list[str]]:
    profile = load_profile()
    resume = normalize(load_master_resume())
    skills = [normalize(s) for s in profile.get("skills", [])]
    tools = [normalize(t) for t in profile.get("tools", [])]
    evidence: list[str] = []
    skill_hits = [s for s in skills if s and s in blob]
    tool_hits = [t for t in tools if t and t in blob]
    jd_tokens = {w for w in blob.split() if len(w) > 4}
    resume_tokens = set(resume.split())
    overlap = len(jd_tokens & resume_tokens)
    score = min(55.0, len(skill_hits) * 7.0 + len(tool_hits) * 8.0)
    score += min(35.0, overlap * 0.35)
    if skill_hits:
        evidence.append("Resume skills cited in JD: " + ", ".join(skill_hits[:6]))
    if tool_hits:
        evidence.append("Resume tools cited in JD: " + ", ".join(tool_hits[:5]))
    if not evidence:
        evidence.append("Limited direct resume↔JD keyword overlap")
    return max(0.0, min(100.0, score)), evidence


def _portfolio_score(job: dict[str, Any], projects: list[dict[str, Any]] | None = None) -> tuple[float, list[str]]:
    projects = projects if projects is not None else match_portfolio(job)
    if not projects:
        return 20.0, ["No strong portfolio keyword overlap yet"]
    top = projects[0]
    score = min(100.0, 40.0 + len(projects) * 15.0)
    evidence = [f"Cite: {p.get('name')} ({p.get('url')})" for p in projects[:4]]
    if top.get("blurb"):
        evidence.insert(0, f"Strongest project: {top.get('name')} — {top.get('blurb')}")
    return score, evidence


def _interview_readiness_score(job: dict[str, Any], blob: str, title: str) -> tuple[float, list[str]]:
    """
    Explainable readiness signals only — NOT a forecast of interview odds.
    Combines level fit, title priority, and absence of senior/years gates.
    """
    evidence: list[str] = []
    if requires_five_plus_years(job):
        return 15.0, ["Hard 5+ years requirement — low readiness vs verified profile"]
    score = 50.0
    if priority_title_hit(job):
        score += 25
        evidence.append("Priority target-role title")
    if any(k in title or k in blob for k in LEVEL_KEYWORDS):
        score += 15
        evidence.append("Entry/junior/associate/specialist language present")
    if any(k in title for k in ["senior", "staff", "principal", "director", "lead "]):
        score = min(score, 25.0)
        evidence.append("Senior-leaning title reduces readiness score")
    if "manager" in title and "associate" not in title:
        score = min(score, 20.0)
        evidence.append("Manager title outside honest-fit band")
    if not evidence:
        evidence.append("Neutral level signals — readiness from role/keyword overlap only")
    evidence.append("This is an explainable readiness component — not a predicted interview probability.")
    return max(0.0, min(100.0, score)), evidence


def _career_growth_score(job: dict[str, Any], blob: str) -> tuple[float, list[str]]:
    evidence: list[str] = []
    score = 40.0
    growth_terms = [
        "career growth",
        "learning",
        "mentorship",
        "path to",
        "enablement",
        "implementation",
        "ownership",
        "impact",
    ]
    hits = [t for t in growth_terms if t in blob]
    score += min(40.0, len(hits) * 8.0)
    if priority_title_hit(job):
        score += 15
        evidence.append("Target role family supports long-term AI Ops path")
    if hits:
        evidence.append("Growth language in JD: " + ", ".join(hits[:4]))
    if not evidence:
        evidence.append("Limited explicit growth language — neutral")
    return max(0.0, min(100.0, score)), evidence


def _remote_score(job: dict[str, Any]) -> tuple[float, list[str]]:
    v = verify_remote(job)
    if v["verified"]:
        return 100.0, [v["label"] + " — " + v["reason"]]
    return 0.0, [v["label"] + " — " + v["reason"]]


def _salary_score(job: dict[str, Any], floor: float = 60000) -> tuple[float, list[str]]:
    mid = salary_mid(job)
    text = (job.get("salary_text") or "").strip()
    if mid is None and not text:
        return 50.0, ["Salary not listed — neutral (not invented)"]
    if mid is None:
        return 55.0, [f"Salary text listed: {text} (range not parsed)"]
    if mid < floor:
        return 20.0, [f"Listed mid ~${mid:,.0f} is below ${floor:,.0f} floor"]
    if mid < 70000:
        score = 60.0
    elif mid < 90000:
        score = 80.0
    elif mid < 120000:
        score = 92.0
    else:
        score = 100.0
    return score, [f"Listed compensation mid ~${mid:,.0f}"]


def score_job(job: dict[str, Any]) -> tuple[float, dict[str, Any]]:
    blob = text_blob(job)
    title = normalize(job.get("title", ""))
    projects = match_portfolio(job)

    skill, skill_ev = _skill_score(job, blob, title)
    interview_ready, ir_ev = _interview_readiness_score(job, blob, title)
    remote, remote_ev = _remote_score(job)
    salary, sal_ev = _salary_score(job)
    growth, growth_ev = _career_growth_score(job, blob)
    resume, resume_ev = _resume_score(job, blob)
    portfolio, port_ev = _portfolio_score(job, projects)

    total = (
        skill * W_SKILL
        + interview_ready * W_INTERVIEW_READINESS
        + remote * W_REMOTE
        + salary * W_SALARY
        + growth * W_CAREER_GROWTH
        + resume * W_RESUME
        + portfolio * W_PORTFOLIO
    )
    total = max(1.0, min(100.0, round(total, 1)))

    mid = salary_mid(job)
    breakdown = {
        "match_score": total,
        "match_percentage": total,
        "components": {
            "skill_match": {"score": round(skill, 1), "weight": W_SKILL, "evidence": skill_ev},
            "interview_readiness": {
                "score": round(interview_ready, 1),
                "weight": W_INTERVIEW_READINESS,
                "evidence": ir_ev,
            },
            "remote_eligibility": {"score": round(remote, 1), "weight": W_REMOTE, "evidence": remote_ev},
            "salary_fit": {"score": round(salary, 1), "weight": W_SALARY, "evidence": sal_ev},
            "career_growth": {"score": round(growth, 1), "weight": W_CAREER_GROWTH, "evidence": growth_ev},
            "resume_match": {"score": round(resume, 1), "weight": W_RESUME, "evidence": resume_ev},
            "portfolio_match": {"score": round(portfolio, 1), "weight": W_PORTFOLIO, "evidence": port_ev},
            # Legacy alias for UI bars that still look for experience_fit
            "experience_fit": {
                "score": round(interview_ready, 1),
                "weight": W_INTERVIEW_READINESS,
                "evidence": ir_ev,
                "alias_of": "interview_readiness",
            },
        },
        "skill_match": round(skill, 1),
        "interview_readiness": round(interview_ready, 1),
        "resume_match": round(resume, 1),
        "portfolio_match": round(portfolio, 1),
        "experience_fit": round(interview_ready, 1),
        "remote_eligibility": round(remote, 1),
        "salary_fit": round(salary, 1),
        "career_growth": round(growth, 1),
        "weights": {
            "skill_match": W_SKILL,
            "interview_readiness": W_INTERVIEW_READINESS,
            "remote_eligibility": W_REMOTE,
            "salary_fit": W_SALARY,
            "career_growth": W_CAREER_GROWTH,
            "resume_match": W_RESUME,
            "portfolio_match": W_PORTFOLIO,
        },
        "estimated_salary_mid": mid,
        "total": total,
        "interview_probability": None,
        "scoring_mode": "transparent_match_score_v2",
        "note": "Match Score v2 is a transparent weighted fit score. interview_readiness is NOT a predicted interview rate.",
    }
    return total, breakdown
