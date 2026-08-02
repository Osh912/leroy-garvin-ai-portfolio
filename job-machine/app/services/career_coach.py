from __future__ import annotations

"""
AI Career Coach — improvement analysis from real tracked data only.
Never invents experience, education, or certifications.
"""

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.config import MASTER_RESUME, ROOT
from app.models import Application, Job
from app.services.career_agent import TECH_VOCAB, _skill_gaps
from app.services.filters import load_portfolio, load_profile, normalize
from app.services.pipeline_stages import normalize_status
from app.services.truth_guard import scan_for_fabrication

REPORTS_DIR = ROOT / "data" / "weekly_reports"


def analyze_career(db: Session) -> dict[str, Any]:
    profile = load_profile()
    candidate = profile.get("candidate") or {}
    portfolio = load_portfolio()
    jobs = db.query(Job).filter(Job.status.notin_(["inactive", "purged"])).all()
    apps = db.query(Application).all()

    resume_text = ""
    if MASTER_RESUME.exists():
        resume_text = MASTER_RESUME.read_text(encoding="utf-8", errors="ignore")
    # Also sample latest tailored resumes
    for a in sorted(apps, key=lambda x: x.updated_at or datetime.min, reverse=True)[:5]:
        if a.tailored_resume:
            resume_text += "\n" + a.tailored_resume

    missing_skills, freq_tech = _skill_gaps(jobs)
    resume_weak = _resume_weaknesses(resume_text, candidate, profile)
    portfolio_weak = _portfolio_weaknesses(portfolio, freq_tech)
    interview_perf = _interview_performance(apps)
    ats_coverage = _ats_keyword_coverage(resume_text, jobs)
    salary_growth = _salary_growth(apps, jobs)
    truth_flags = scan_for_fabrication(resume_text)

    return {
        "mode": "ai_career_coach",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "fabricated": False,
        "auto_apply": False,
        "approval_required": True,
        "resume_weaknesses": resume_weak,
        "portfolio_weaknesses": portfolio_weak,
        "missing_skills": missing_skills,
        "frequently_requested_technologies": freq_tech,
        "interview_performance": interview_perf,
        "ats_keyword_coverage": ats_coverage,
        "salary_growth_opportunities": salary_growth,
        "truth_scan_flags": truth_flags,
        "profile_truth": {
            "education_listed": candidate.get("education") or [],
            "certifications_listed": candidate.get("certifications") or [],
            "note": "Empty education/certifications means none — never invent them.",
        },
    }


def weekly_improvement_report(db: Session) -> dict[str, Any]:
    analysis = analyze_career(db)
    actions = []
    for w in analysis["resume_weaknesses"][:5]:
        actions.append({"area": "resume", "action": w, "approval_required": True})
    for w in analysis["portfolio_weaknesses"][:5]:
        actions.append({"area": "portfolio", "action": w, "approval_required": True})
    for m in analysis["missing_skills"][:5]:
        actions.append(
            {
                "area": "skills",
                "action": f"Consider learning/demo for “{m['skill_or_tech']}” ({m['job_mentions']} mentions) — only claim after real evidence.",
                "approval_required": True,
            }
        )
    for tip in (analysis["ats_keyword_coverage"].get("recommendations") or [])[:5]:
        actions.append({"area": "ats", "action": tip, "approval_required": True})
    for tip in (analysis["salary_growth_opportunities"].get("recommendations") or [])[:3]:
        actions.append({"area": "salary", "action": tip, "approval_required": True})

    report = {
        "mode": "weekly_improvement_report",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "fabricated": False,
        "auto_apply": False,
        "auto_email": False,
        "approval_required": True,
        "summary": analysis,
        "recommended_actions": actions,
        "notes": [
            "All recommendations require Leroy’s approval before changing applications or outreach.",
            "Do not add degrees or certifications not in profile.json.",
        ],
    }
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / f"weekly_{datetime.utcnow().date().isoformat()}.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    (REPORTS_DIR / "latest.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def load_latest_weekly_report() -> dict[str, Any] | None:
    path = REPORTS_DIR / "latest.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _resume_weaknesses(text: str, candidate: dict[str, Any], profile: dict[str, Any]) -> list[str]:
    weaknesses: list[str] = []
    t = normalize(text)
    if "bachelor" in t or "master" in t or "phd" in t:
        if not (candidate.get("education") or []):
            weaknesses.append("Resume text may imply degrees — profile lists none. Remove any degree claims.")
    if not candidate.get("certifications") and re.search(r"\bcertified\b|\bcertification\b", t):
        weaknesses.append("Certification language detected while profile certifications are empty — verify or remove.")
    if "portfolio" not in t and "leroy-garvin-ai-portfolio" not in t:
        weaknesses.append("Master/tailored resume samples often omit explicit portfolio URL — add verified portfolio link.")
    if "linkedin.com" not in t:
        weaknesses.append("LinkedIn URL not consistently present in resume samples.")
    skills = profile.get("skills") or []
    if skills and sum(1 for s in skills if normalize(s) in t) < max(3, len(skills) // 4):
        weaknesses.append("Few verified profile skills appear in resume samples — mirror exact skill wording from profile.json.")
    if "senior engineer" in t:
        weaknesses.append("Forbidden claim pattern “senior engineer” — remove immediately.")
    if not weaknesses:
        weaknesses.append("No critical fabrication flags in sampled resume text; keep quantifying with portfolio metrics only.")
    return weaknesses


def _portfolio_weaknesses(portfolio: list[dict[str, Any]], freq_tech: list[dict[str, Any]]) -> list[str]:
    weaknesses: list[str] = []
    if not portfolio:
        return ["No portfolio projects loaded — add verified projects only."]
    names = " ".join(normalize(p.get("name", "")) for p in portfolio)
    blurbs = " ".join(normalize(p.get("blurb", "")) for p in portfolio)
    blob = names + " " + blurbs
    top_tech = [x["technology"] for x in freq_tech[:8]]
    missing_demo = [t for t in top_tech if t not in blob and t not in {"api", "rest"}]
    if missing_demo:
        weaknesses.append(
            "Frequent posting tech with weak portfolio mention: "
            + ", ".join(missing_demo[:6])
            + " — only add demos you actually build."
        )
    for p in portfolio:
        if not p.get("metrics"):
            weaknesses.append(f"Project “{p.get('name')}” lacks metrics array — add truthful measurable outcomes only.")
        if not p.get("url"):
            weaknesses.append(f"Project “{p.get('name')}” missing URL.")
    if len(portfolio) < 3:
        weaknesses.append("Fewer than 3 portfolio projects — expand with real work only.")
    if not weaknesses:
        weaknesses.append("Portfolio structure looks usable; keep LawOne labeled in-development when mentioned.")
    return weaknesses


def _interview_performance(apps: list[Application]) -> dict[str, Any]:
    behavioral_pass = behavioral_total = 0
    technical_pass = technical_total = 0
    weak: Counter = Counter()
    strong: Counter = Counter()
    for a in apps:
        try:
            meta = json.loads(a.analytics_json or "{}")
        except json.JSONDecodeError:
            meta = {}
        ia = meta.get("interview_analytics") or {}
        if ia.get("behavioral_result") in {"pass", "fail"}:
            behavioral_total += 1
            if ia.get("behavioral_result") == "pass":
                behavioral_pass += 1
        if ia.get("technical_result") in {"pass", "fail"}:
            technical_total += 1
            if ia.get("technical_result") == "pass":
                technical_pass += 1
        for t in ia.get("weak_topics") or []:
            if isinstance(t, str) and t.strip():
                weak[t.strip()] += 1
        for t in ia.get("strong_topics") or []:
            if isinstance(t, str) and t.strip():
                strong[t.strip()] += 1
        for lesson in meta.get("lessons_learned") or []:
            if lesson.get("what_to_improve"):
                weak[lesson["what_to_improve"][:120]] += 1
            if lesson.get("what_went_well"):
                strong[lesson["what_went_well"][:120]] += 1

    def rate(p: int, t: int) -> float | None:
        return round(100.0 * p / t, 1) if t else None

    return {
        "behavioral_pass_rate": rate(behavioral_pass, behavioral_total),
        "technical_pass_rate": rate(technical_pass, technical_total),
        "samples_behavioral": behavioral_total,
        "samples_technical": technical_total,
        "weakest_topics": [{"topic": t, "count": n} for t, n in weak.most_common(8)],
        "strongest_topics": [{"topic": t, "count": n} for t, n in strong.most_common(8)],
        "note": "Rates appear only after Lessons Learned / interview analytics are logged. Null means insufficient data.",
    }


def _ats_keyword_coverage(resume_text: str, jobs: list[Job]) -> dict[str, Any]:
    blob = normalize(resume_text)
    counts: Counter = Counter()
    for j in jobs[:80]:
        text = normalize(f"{j.title} {j.tags}")
        for tech in TECH_VOCAB:
            if re.search(rf"\b{re.escape(tech)}\b", text):
                counts[tech] += 1
    covered = []
    missing = []
    for tech, n in counts.most_common(20):
        if re.search(rf"\b{re.escape(tech)}\b", blob):
            covered.append({"keyword": tech, "job_mentions": n})
        else:
            missing.append({"keyword": tech, "job_mentions": n})
    recommendations = []
    for m in missing[:6]:
        recommendations.append(
            f"If truthful, mention “{m['keyword']}” where you have real evidence ({m['job_mentions']} job mentions)."
        )
    if not recommendations:
        recommendations.append("Resume already covers many frequent keywords from tracked jobs.")
    return {
        "covered": covered[:12],
        "missing_from_resume_samples": missing[:12],
        "recommendations": recommendations,
    }


def _salary_growth(apps: list[Application], jobs: list[Job]) -> dict[str, Any]:
    listed = []
    for j in jobs:
        if j.salary_min:
            listed.append(float(j.salary_min))
    interview_sals = []
    for a in apps:
        st = normalize_status(a.status)
        if st in {"phone_screen", "technical_interview", "hiring_manager", "final_interview", "offer"}:
            # parse crude numbers from salary field
            nums = re.findall(r"(\d{2,3}),?(\d{3})", a.salary or "")
            if nums:
                interview_sals.append(float(nums[0][0] + nums[0][1]))
    recs = []
    if listed:
        avg = sum(listed) / len(listed)
        recs.append(f"Tracked postings with min salary average ~${avg:,.0f} (listed mins only).")
        recs.append("Target roles listing $80k–$100k+ when Match Score is strong — do not invent counter-offers.")
    else:
        recs.append("Insufficient listed salary data for trend advice.")
    if interview_sals:
        recs.append(f"Interview-stage apps show salary text around ${sum(interview_sals)/len(interview_sals):,.0f} average (parsed from recorded text).")
    return {
        "listed_min_samples": len(listed),
        "interview_stage_salary_samples": len(interview_sals),
        "recommendations": recs,
    }
