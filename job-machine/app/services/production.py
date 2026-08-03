from __future__ import annotations

"""Production Mode — block placeholders, require live posting metadata."""

import re
from typing import Any
from urllib.parse import urlparse

from app.services.filters import normalize

PLACEHOLDER_COMPANIES = {
    "acme",
    "acme ai",
    "acme ai.",
    "example co",
    "example corp",
    "example company",
    "demo company",
    "demo corp",
    "test company",
    "test corp",
    "sample company",
    "sample corp",
    "placeholder",
    "fake company",
    "unknown",
    "n/a",
    "none",
    "company name",
    "your company",
}

PLACEHOLDER_PATTERNS = [
    r"^acme\b",
    r"^example\b",
    r"^demo\b",
    r"^test\b",
    r"^sample\b",
    r"^placeholder\b",
    r"^foo\b",
    r"^bar\b",
]


def is_placeholder_company(company: str) -> bool:
    c = normalize(company)
    if not c or c in PLACEHOLDER_COMPANIES:
        return True
    if any(re.search(p, c) for p in PLACEHOLDER_PATTERNS):
        return True
    return False


def has_valid_posting_url(url: str) -> bool:
    u = (url or "").strip()
    if not u:
        return False
    parsed = urlparse(u)
    if parsed.scheme not in {"http", "https"}:
        return False
    host = (parsed.netloc or "").lower()
    if not host or host in {"example.com", "localhost", "127.0.0.1"}:
        return False
    return True


def careers_url_for_job(job: dict[str, Any]) -> str:
    """Derive official careers/board URL from source + posting URL when possible."""
    source = str(job.get("source") or "")
    url = (job.get("url") or "").strip()
    company = normalize(job.get("company", ""))

    if source.startswith("greenhouse:"):
        board = source.split(":", 1)[1]
        return f"https://boards.greenhouse.io/{board}"
    if source.startswith("lever:"):
        board = source.split(":", 1)[1]
        return f"https://jobs.lever.co/{board}"
    if source.startswith("ashby:"):
        board = source.split(":", 1)[1]
        return f"https://jobs.ashbyhq.com/{board}"
    if source.startswith("workable:"):
        board = source.split(":", 1)[1]
        return f"https://apply.workable.com/{board}"
    if source == "remoteok":
        return "https://remoteok.com"
    if source == "remotive":
        return "https://remotive.com"
    if source == "jobicy":
        return "https://jobicy.com"
    if source == "arbeitnow":
        return "https://www.arbeitnow.com"
    # Paid boards never returned as careers destinations
    if source in {"weworkremotely", "flexjobs", "remoterocketship"}:
        return ""

    # Fallback: origin of posting URL
    if url:
        parsed = urlparse(url)
        if parsed.scheme and parsed.netloc:
            return f"{parsed.scheme}://{parsed.netloc}"

    # Known company careers pages (display aid only — posting URL remains primary)
    known = {
        "stripe": "https://stripe.com/jobs",
        "datadog": "https://careers.datadoghq.com",
        "anthropic": "https://www.anthropic.com/careers",
        "openai": "https://openai.com/careers",
        "gitlab": "https://about.gitlab.com/jobs",
        "airtable": "https://airtable.com/careers",
        "automattic": "https://automattic.com/work-with-us",
        "zapier": "https://zapier.com/jobs",
        "hubspot": "https://www.hubspot.com/careers",
        "cloudflare": "https://www.cloudflare.com/careers",
        "mozilla": "https://www.mozilla.org/careers",
        "elastic": "https://www.elastic.co/careers",
        "canonical": "https://canonical.com/careers",
    }
    for key, careers in known.items():
        if key in company:
            return careers
    return url


def is_production_eligible(job: dict[str, Any]) -> tuple[bool, str]:
    """Return (ok, reason). Reject placeholders and URL-less fake rows."""
    company = (job.get("company") or "").strip()
    if is_placeholder_company(company):
        return False, "placeholder_company"
    if not has_valid_posting_url(str(job.get("url") or "")):
        return False, "missing_or_invalid_posting_url"
    title = (job.get("title") or "").strip()
    if not title or normalize(title) in {"untitled", "test", "demo"}:
        return False, "invalid_title"
    return True, "ok"


def source_display(source: str) -> str:
    s = (source or "").strip()
    if not s:
        return "Unknown"
    if s.startswith("greenhouse:"):
        return f"Greenhouse ({s.split(':', 1)[1]})"
    if s.startswith("lever:"):
        return f"Lever ({s.split(':', 1)[1]})"
    if s.startswith("ashby:"):
        return f"Ashby ({s.split(':', 1)[1]})"
    if s.startswith("workable:"):
        return f"Workable ({s.split(':', 1)[1]})"
    mapping = {
        "remoteok": "RemoteOK (free)",
        "remotive": "Remotive (free)",
        "jobicy": "Jobicy (free)",
        "arbeitnow": "Arbeitnow (free)",
        "manual": "Manual Import (free)",
        "linkedin": "LinkedIn Easy Apply (free)",
        "indeed": "Indeed (free)",
        "ziprecruiter": "ZipRecruiter (free)",
        "builtin": "Built In (free)",
        "wellfound": "Wellfound (free)",
        "otta": "Otta (free)",
        "weworkremotely": "BLOCKED — We Work Remotely (paid/auto-apply)",
        "flexjobs": "BLOCKED — FlexJobs (paid)",
        "remoterocketship": "BLOCKED — Remote Rocketship (paid)",
    }
    return mapping.get(s.lower(), s)
