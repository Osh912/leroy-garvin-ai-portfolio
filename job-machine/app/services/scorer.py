from __future__ import annotations

"""
PRODUCTION MODE — Transparent Match Score.

Never invents interview probability percentages.
Match Score = weighted average of documented components (each 0–100):

  25% Skill match
  20% Resume match
  20% Portfolio match
  15% Required experience fit
  10% Remote eligibility
  10% Salary fit
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

W_SKILL = 0.25
W_RESUME = 0.20
W_PORTFOLIO = 0.20
W_EXPERIENCE = 0.15
W_REMOTE = 0.10
W_SALARY = 0.10

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
    # Also check resume text overlap with JD distinctive tokens
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
    # match_portfolio returns relevance-ish ordering; score by count + top strength
    score = min(100.0, 40.0 + len(projects) * 15.0)
    evidence = [f"Cite: {p.get('name')} ({p.get('url')})" for p in projects[:4]]
    if top.get("blurb"):
        evidence.insert(0, f"Strongest project: {top.get('name')} — {top.get('blurb')}")
    return score, evidence


def _experience_score(job: dict[str, Any], blob: str, title: str) -> tuple[float, list[str]]:
    evidence: list[str] = []
    if requires_five_plus_years(job):
        return 15.0, ["Hard 5+ years requirement — poor fit for current verified profile"]
    score = 55.0
    if any(k in title or k in blob for k in LEVEL_KEYWORDS):
        score = 90.0
        evidence.append("Level language fits entry / junior / associate / specialist")
    if any(k in title for k in ["senior", "staff", "principal", "director", "lead "]):
        score = min(score, 25.0)
        evidence.append("Title leans senior — stretch vs verified experience")
    if "manager" in title and "associate" not in title:
        score = min(score, 20.0)
        evidence.append("Manager title — outside honest-fit band")
    if not evidence:
        evidence.append("No hard senior years gate detected; mid/unspecified level")
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
    resume, resume_ev = _resume_score(job, blob)
    portfolio, port_ev = _portfolio_score(job, projects)
    experience, exp_ev = _experience_score(job, blob, title)
    remote, remote_ev = _remote_score(job)
    salary, sal_ev = _salary_score(job)

    total = (
        skill * W_SKILL
        + resume * W_RESUME
        + portfolio * W_PORTFOLIO
        + experience * W_EXPERIENCE
        + remote * W_REMOTE
        + salary * W_SALARY
    )
    total = max(1.0, min(100.0, round(total, 1)))

    mid = salary_mid(job)
    breakdown = {
        "match_score": total,
        "match_percentage": total,
        "components": {
            "skill_match": {"score": round(skill, 1), "weight": W_SKILL, "evidence": skill_ev},
            "resume_match": {"score": round(resume, 1), "weight": W_RESUME, "evidence": resume_ev},
            "portfolio_match": {"score": round(portfolio, 1), "weight": W_PORTFOLIO, "evidence": port_ev},
            "experience_fit": {"score": round(experience, 1), "weight": W_EXPERIENCE, "evidence": exp_ev},
            "remote_eligibility": {"score": round(remote, 1), "weight": W_REMOTE, "evidence": remote_ev},
            "salary_fit": {"score": round(salary, 1), "weight": W_SALARY, "evidence": sal_ev},
        },
        # Flat keys for older UI paths
        "skill_match": round(skill, 1),
        "resume_match": round(resume, 1),
        "portfolio_match": round(portfolio, 1),
        "experience_fit": round(experience, 1),
        "remote_eligibility": round(remote, 1),
        "salary_fit": round(salary, 1),
        "weights": {
            "skill_match": W_SKILL,
            "resume_match": W_RESUME,
            "portfolio_match": W_PORTFOLIO,
            "experience_fit": W_EXPERIENCE,
            "remote_eligibility": W_REMOTE,
            "salary_fit": W_SALARY,
        },
        "estimated_salary_mid": mid,
        "total": total,
        # Explicitly not an interview probability forecast
        "interview_probability": None,
        "scoring_mode": "transparent_match_score_v1",
        "note": "Match Score is a transparent weighted fit score — not a predicted interview rate.",
    }
    return total, breakdown
