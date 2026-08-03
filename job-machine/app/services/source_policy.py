from __future__ import annotations

"""
Free-source policy for Career OS job finder.

Never search, recommend, or open paid/subscription job boards.
Only free employer ATS postings and free apply surfaces.
"""

import re
from typing import Any
from urllib.parse import urlparse

from app.services.filters import normalize, text_blob

# Permanently blocked — paid subscription / premium / pay-to-apply boards
PAID_BOARD_HOSTS = {
    "flexjobs.com",
    "www.flexjobs.com",
    "remoterocketship.com",
    "www.remoterocketship.com",
    "weworkremotely.com",
    "www.weworkremotely.com",
    # WWR AI Auto-Apply and related paid funnels
    "auto-apply.weworkremotely.com",
    "ai.weworkremotely.com",
}

PAID_BOARD_SOURCE_KEYS = {
    "weworkremotely",
    "wwr",
    "flexjobs",
    "flex_jobs",
    "remoterocketship",
    "remote_rocketship",
    "remote-rocketship",
}

PAID_BOARD_NAME_PATTERNS = [
    r"\bflexjobs\b",
    r"\bflex jobs\b",
    r"\bremote rocketship\b",
    r"\bremoterocketship\b",
    r"\bwe work remotely\b",
    r"\bweworkremotely\b",
    r"\bwwr\b.*\bauto[- ]?apply\b",
    r"\bai auto[- ]?apply\b",
    r"\bpaid (job )?board\b",
    r"\bpremium membership\b",
    r"\bsubscribe to apply\b",
    r"\bunlock (this )?job\b",
    r"\bpay to apply\b",
    r"\bpayment required to apply\b",
]

# Free ATS / employer hosts (and free aggregators that deep-link to free apply)
ALLOWED_FREE_HOST_FRAGMENTS = {
    # ATS
    "greenhouse.io",
    "lever.co",
    "ashbyhq.com",
    "myworkdayjobs.com",
    "workday.com",
    "smartrecruiters.com",
    "icims.com",
    "taleo.net",
    "bamboohr.com",
    "rippling.com",
    "teamtailor.com",
    "personio.com",
    "personio.de",
    "jobvite.com",
    "oraclecloud.com",
    "workable.com",
    # Free aggregators / discovery (never paywalled apply)
    "remoteok.com",
    "remotive.com",
    "jobicy.com",
    "arbeitnow.com",
    "linkedin.com",
    "indeed.com",
    "ziprecruiter.com",
    "google.com",
    "builtin.com",
    "wellfound.com",
    "angel.co",
    "otta.com",
}

ALLOWED_FREE_SOURCE_PREFIXES = {
    "greenhouse",
    "lever",
    "ashby",
    "workable",
    "workday",
    "smartrecruiters",
    "icims",
    "taleo",
    "bamboohr",
    "rippling",
    "teamtailor",
    "personio",
    "jobvite",
    "oracle",
    "remoteok",
    "remotive",
    "jobicy",
    "arbeitnow",
    "linkedin",
    "indeed",
    "ziprecruiter",
    "google_jobs",
    "builtin",
    "wellfound",
    "otta",
    "manual",
    "careers",
    "company",
}

# Staffing / RPO agencies — reject unless a clear employer is named
STAFFING_AGENCY_PATTERNS = [
    r"\bstaffing\b",
    r"\bstaffing agency\b",
    r"\brecruiting agency\b",
    r"\brecruitment agency\b",
    r"\btalent solutions\b",
    r"\bworkforce solutions\b",
    r"\bcontract staffing\b",
    r"\brpo\b",
    r"\bplacement agency\b",
    r"\bpersonnel services\b",
    r"\btemp agency\b",
]

EMPLOYER_IDENTIFIED_PATTERNS = [
    r"\bon behalf of\b",
    r"\bhiring for\b",
    r"\bclient[:\s]",
    r"\bour client\b",
    r"\bemployer[:\s]",
    r"\bat [A-Z][A-Za-z0-9 .,&-]{2,60}\b",
]


def _host(url: str) -> str:
    try:
        return (urlparse(url or "").hostname or "").lower().removeprefix("www.")
    except Exception:  # noqa: BLE001
        return ""


def is_paid_board_host(host: str) -> bool:
    h = (host or "").lower().removeprefix("www.")
    if not h:
        return False
    if h in {x.removeprefix("www.") for x in PAID_BOARD_HOSTS}:
        return True
    return any(h == b or h.endswith("." + b) for b in ("flexjobs.com", "remoterocketship.com", "weworkremotely.com"))


def is_paid_board_source(source: str) -> bool:
    s = normalize(source or "")
    root = s.split(":")[0]
    if root in PAID_BOARD_SOURCE_KEYS or s in PAID_BOARD_SOURCE_KEYS:
        return True
    blob = s
    return any(re.search(p, blob) for p in PAID_BOARD_NAME_PATTERNS)


def is_paid_board_job(job: dict[str, Any]) -> tuple[bool, str]:
    """True when this listing comes from a paid/subscription board or pay-to-apply funnel."""
    source = str(job.get("source") or "")
    url = str(job.get("url") or "")
    host = _host(url)
    careers = str(job.get("careers_url") or "")
    careers_host = _host(careers)
    blob = text_blob(job)

    if is_paid_board_source(source):
        return True, f"paid_source:{source}"
    if is_paid_board_host(host) or is_paid_board_host(careers_host):
        return True, f"paid_host:{host or careers_host}"
    for pat in PAID_BOARD_NAME_PATTERNS:
        if re.search(pat, blob, re.I) and any(
            x in blob for x in ["subscribe", "membership", "premium", "unlock", "pay to apply", "auto-apply", "auto apply"]
        ):
            return True, f"paid_copy:{pat}"
    # Explicit paywalls in apply copy
    paywall = [
        r"subscribe to (view|apply|unlock)",
        r"premium members? only",
        r"membership required to apply",
        r"upgrade to apply",
        r"payment required before applying",
    ]
    for pat in paywall:
        if re.search(pat, blob, re.I):
            return True, f"paywall:{pat}"
    return False, ""


def is_allowed_free_source(job: dict[str, Any]) -> tuple[bool, str]:
    """
    Allow free ATS, free aggregators, free discovery boards, and direct careers pages.
    Reject unknown paid boards even if not on the named blacklist.
    """
    paid, reason = is_paid_board_job(job)
    if paid:
        return False, reason

    source = str(job.get("source") or "").strip().lower()
    root = source.split(":")[0]
    url = str(job.get("url") or "")
    host = _host(url)

    if root in ALLOWED_FREE_SOURCE_PREFIXES or any(source.startswith(p + ":") for p in ALLOWED_FREE_SOURCE_PREFIXES):
        return True, "allowed_source"

    if any(frag in host for frag in ALLOWED_FREE_HOST_FRAGMENTS):
        return True, "allowed_host"

    # Direct company careers pages (non-blacklisted HTTPS host)
    if host and not is_paid_board_host(host):
        # Treat as direct careers if path looks like careers/jobs/apply
        path = (urlparse(url).path or "").lower()
        if any(x in path for x in ("/careers", "/jobs", "/job/", "/apply", "/positions", "/openings")):
            return True, "direct_careers"
        if root in {"manual", "careers", "company"} or source.startswith("manual"):
            return True, "manual_or_careers"

    return False, f"unsupported_or_unknown_source:{source or host or 'empty'}"


def is_staffing_agency_without_employer(job: dict[str, Any]) -> bool:
    """Reject staffing agencies unless the employer is clearly identified."""
    company = normalize(job.get("company", ""))
    title = normalize(job.get("title", ""))
    blob = text_blob(job)
    company_is_agency = any(re.search(p, company) for p in STAFFING_AGENCY_PATTERNS)
    title_is_agency = any(re.search(p, title) for p in STAFFING_AGENCY_PATTERNS)
    desc_agency = any(re.search(p, blob) for p in STAFFING_AGENCY_PATTERNS[:6])
    if not (company_is_agency or title_is_agency or (desc_agency and company_is_agency)):
        return False
    # Employer clearly identified?
    if any(re.search(p, blob, re.I) for p in EMPLOYER_IDENTIFIED_PATTERNS):
        return False
    # Title like "X at Employer" / "Employer — Role"
    if re.search(r"\bat [a-z0-9].+", title) or " — " in (job.get("title") or "") or " - " in (job.get("title") or ""):
        # Still agency if company itself is only the staffing firm and no client named
        if company_is_agency and not re.search(r"\b(client|behalf|hiring for)\b", blob):
            return True
        return False
    return True


def source_policy_summary() -> dict[str, Any]:
    return {
        "paid_boards_blacklisted": sorted(PAID_BOARD_HOSTS),
        "paid_sources_blacklisted": sorted(PAID_BOARD_SOURCE_KEYS),
        "free_ats_and_boards": sorted(ALLOWED_FREE_SOURCE_PREFIXES),
        "never_recommend_paid_boards": True,
        "auto_apply": False,
        "note": (
            "Only free employer ATS and free apply surfaces. "
            "We Work Remotely / FlexJobs / Remote Rocketship and any pay-to-apply board are permanently excluded. "
            "LinkedIn Easy Apply, Indeed, ZipRecruiter, Google Jobs, Built In, Wellfound, and Otta remain allowed when free."
        ),
    }
