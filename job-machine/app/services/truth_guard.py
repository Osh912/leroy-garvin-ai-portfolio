from __future__ import annotations

import re
from typing import Any

from app.services.filters import load_profile


FORBIDDEN_PATTERNS = [
    r"\b\d+\+?\s+years?\s+of\s+(professional\s+)?(software\s+)?engineering\b",
    r"\bsenior\s+engineer\b",
    r"\bstaff\s+engineer\b",
    r"\bprincipal\s+engineer\b",
    r"\bbachelor'?s\b",
    r"\bmaster'?s\b",
    r"\bph\.?d\b",
    r"\baws\s+certified\b",
    r"\$\d+(\.\d+)?\s*(m|million)\b",
    r"\b\d{3,}\s+customers\b",
    r"\bincreased\s+revenue\b",
]


def scan_for_fabrication(text: str) -> list[str]:
    warnings: list[str] = []
    profile = load_profile()
    lowered = text.lower()
    for claim in profile.get("forbidden_claims", []):
        if claim.lower() in lowered:
            warnings.append(f"Possible forbidden claim: {claim}")
    for pat in FORBIDDEN_PATTERNS:
        if re.search(pat, text, flags=re.I):
            warnings.append(f"Pattern flagged: {pat}")
    # LawOne finished product claim
    if re.search(r"lawone.{0,40}(launched|production|commercially available)", text, flags=re.I):
        warnings.append("LawOne must not be described as a finished commercial product")
    return warnings


def truth_system_prompt() -> str:
    profile = load_profile()
    rules = "\n".join(f"- {r}" for r in profile.get("truth_rules", []))
    forbidden = ", ".join(profile.get("forbidden_claims", []))
    return (
        "You are helping Leroy Garvin Jr apply for jobs. "
        "Use ONLY verified facts from the provided master resume and profile. "
        "Never invent employers, degrees, certifications, revenue, customer counts, or years of experience. "
        "Never claim senior engineering experience. "
        f"Forbidden claims: {forbidden}.\n"
        f"Rules:\n{rules}"
    )
