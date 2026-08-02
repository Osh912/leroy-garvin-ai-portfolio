from __future__ import annotations

"""Interview Pipeline constants and stage helpers."""

from typing import Any

# Interview Tracker stages (never auto-apply — Applied requires explicit approval)
PIPELINE_STAGES = [
    "saved",
    "ready",  # packet prepared, awaiting Leroy's apply approval
    "applied",
    "recruiter_contact",
    "first_interview",
    "technical_interview",
    "final_interview",
    "offer",
    "rejected",
]

STAGE_LABELS = {
    "saved": "Saved",
    "ready": "Ready (awaiting approval)",
    "applied": "Applied",
    "recruiter_contact": "Recruiter Contact",
    "first_interview": "First Interview",
    "technical_interview": "Technical Interview",
    "final_interview": "Final Interview",
    "offer": "Offer",
    "rejected": "Rejected",
}

INTERVIEW_STAGES = {
    "first_interview",
    "technical_interview",
    "final_interview",
    "recruiter_contact",
}

TARGET_INTERVIEW_ROLES = [
    "ai operations",
    "workflow automation",
    "technical support",
    "solutions engineer",
    "customer success engineer",
    "customer success",
    "ai implementation",
    "automation specialist",
    "implementation specialist",
    "support engineer",
    "support specialist",
]

PORTFOLIO_URL = "https://leroy-garvin-ai-portfolio.vercel.app"


def stage_label(status: str) -> str:
    return STAGE_LABELS.get(status, status.replace("_", " ").title())


def is_interview_stage(status: str) -> bool:
    return status in INTERVIEW_STAGES


def interview_probability_from_job(job: dict[str, Any] | Any) -> float:
    if isinstance(job, dict):
        if job.get("interview_probability") is not None:
            return float(job["interview_probability"])
        bd = job.get("score_breakdown") or {}
        if isinstance(bd, str):
            import json

            try:
                bd = json.loads(bd)
            except Exception:  # noqa: BLE001
                bd = {}
        return float(bd.get("interview_probability") or job.get("score") or 0)
    # ORM Job
    import json

    try:
        bd = json.loads(getattr(job, "score_breakdown", None) or "{}")
    except Exception:  # noqa: BLE001
        bd = {}
    return float(bd.get("interview_probability") or getattr(job, "score", 0) or 0)
