from __future__ import annotations

"""Interview Pipeline constants and stage helpers (Recruiter Analytics Mode)."""

from typing import Any

# Full tracker stages (Applied still requires explicit approval)
PIPELINE_STAGES = [
    "saved",
    "ready",
    "applied",
    "recruiter_viewed",
    "recruiter_replied",
    "phone_screen",
    "technical_interview",
    "hiring_manager",
    "final_interview",
    "offer",
    "accepted",
    "rejected",
    "withdrawn",
]

# Legacy aliases kept so existing data/UI never break
STAGE_ALIASES = {
    "recruiter_contact": "recruiter_replied",
    "first_interview": "phone_screen",
    "interview": "phone_screen",
}

STAGE_LABELS = {
    "saved": "Saved",
    "ready": "Ready",
    "applied": "Applied",
    "recruiter_viewed": "Recruiter Viewed",
    "recruiter_replied": "Recruiter Replied",
    "phone_screen": "Phone Screen",
    "technical_interview": "Technical Interview",
    "hiring_manager": "Hiring Manager",
    "final_interview": "Final Interview",
    "offer": "Offer",
    "accepted": "Accepted",
    "rejected": "Rejected",
    "withdrawn": "Withdrawn",
    # legacy labels
    "recruiter_contact": "Recruiter Replied",
    "first_interview": "Phone Screen",
}

INTERVIEW_STAGES = {
    "phone_screen",
    "technical_interview",
    "hiring_manager",
    "final_interview",
    "first_interview",  # legacy → phone_screen
}

REPLY_STAGES = {
    "recruiter_viewed",
    "recruiter_replied",
    "recruiter_contact",
    "phone_screen",
    "technical_interview",
    "hiring_manager",
    "final_interview",
    "offer",
    "accepted",
}

APPLIED_OR_LATER = {
    "applied",
    "recruiter_viewed",
    "recruiter_replied",
    "recruiter_contact",
    "phone_screen",
    "first_interview",
    "technical_interview",
    "hiring_manager",
    "final_interview",
    "offer",
    "accepted",
    "rejected",
    "withdrawn",
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

ALL_VALID_STATUSES = set(PIPELINE_STAGES) | set(STAGE_ALIASES.keys())


def normalize_status(status: str) -> str:
    s = (status or "saved").strip().lower().replace(" ", "_")
    return STAGE_ALIASES.get(s, s)


def stage_label(status: str) -> str:
    s = normalize_status(status)
    return STAGE_LABELS.get(status, STAGE_LABELS.get(s, s.replace("_", " ").title()))


def is_interview_stage(status: str) -> bool:
    return normalize_status(status) in {
        "phone_screen",
        "technical_interview",
        "hiring_manager",
        "final_interview",
    } or status in INTERVIEW_STAGES


def is_valid_status(status: str) -> bool:
    return (status or "") in ALL_VALID_STATUSES or normalize_status(status) in PIPELINE_STAGES


def interview_probability_from_job(job: dict[str, Any] | Any) -> float:
    """Legacy helper — returns Match Score when interview % is absent."""
    if isinstance(job, dict):
        if job.get("match_score") is not None:
            return float(job["match_score"])
        if job.get("interview_probability") is not None:
            return float(job["interview_probability"])
        bd = job.get("score_breakdown") or {}
        if isinstance(bd, str):
            import json

            try:
                bd = json.loads(bd)
            except Exception:  # noqa: BLE001
                bd = {}
        return float(bd.get("match_score") or bd.get("match_percentage") or job.get("score") or 0)
    import json

    try:
        bd = json.loads(getattr(job, "score_breakdown", None) or "{}")
    except Exception:  # noqa: BLE001
        bd = {}
    return float(bd.get("match_score") or getattr(job, "score", 0) or 0)
