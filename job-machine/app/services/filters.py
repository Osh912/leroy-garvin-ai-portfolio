from __future__ import annotations

import json
import re
from typing import Any

from app.config import TRUTH_DIR, MASTER_RESUME

ROLE_KEYWORDS = [
    "ai operations",
    "automation",
    "workflow",
    "technical support",
    "solutions engineer",
    "customer success",
    "customer success engineer",
    "ai implementation",
    "implementation specialist",
    "automation specialist",
    "ai support",
    "no-code",
    "low-code",
    "n8n",
    "airtable",
    "prompt",
    "conversational",
    "operations specialist",
    "process automation",
    "rpa",
    "zapier",
    "make.com",
]

PRIORITY_TITLE_TERMS = [
    "ai operations",
    "workflow automation",
    "technical support",
    "ai implementation",
    "solutions engineer",
    "customer success engineer",
    "customer success",
    "automation specialist",
    "ai support",
    "automation engineer",
    "implementation specialist",
    "operations specialist",
    "support specialist",
    "support engineer",
]

LEVEL_KEYWORDS = [
    "entry",
    "entry-level",
    "entry level",
    "junior",
    "associate",
    "early career",
    "new grad",
    "coordinator",
    "specialist",
    "support",
]

REMOTE_KEYWORDS = ["remote", "work from home", "wfh", "anywhere", "distributed"]
US_KEYWORDS = ["united states", "usa", "u.s.", "us-only", "us only", "america"]

# STRICT REMOTE MODE — only these (and close variants) verify as fully remote
VERIFIED_REMOTE_PHRASES = [
    "fully remote",
    "100% remote",
    "100 percent remote",
    "remote - united states",
    "remote – united states",
    "remote — united states",
    "remote, united states",
    "remote united states",
    "us remote",
    "u.s. remote",
    "remote us",
    "remote-us",
    "remote (us)",
    "remote (united states)",
    "work from home",
    "work-from-home",
    "wfh",
    "remote only",
    "remote-only",
    "remote first",
    "remote-first",
]

# Trusted remote-only job boards (listings are remote by platform, still need no city/office trap)
TRUSTED_REMOTE_SOURCES = {
    "remoteok",
    "remotive",
    "jobicy",
    "weworkremotely",
    "arbeitnow",
}

REMOTE_LIKE_LOCATIONS = {
    "",
    "remote",
    "worldwide",
    "anywhere",
    "global",
    "usa",
    "u.s.",
    "us",
    "united states",
    "united states of america",
    "remote usa",
    "remote, usa",
    "remote us",
    "work from home",
    "wfh",
}

CITY_MARKERS = [
    "san francisco",
    "sf bay",
    "bay area",
    "new york",
    "nyc",
    "brooklyn",
    "manhattan",
    "boston",
    "seattle",
    "austin",
    "denver",
    "chicago",
    "los angeles",
    "la,",
    "miami",
    "atlanta",
    "dallas",
    "houston",
    "phoenix",
    "philadelphia",
    "washington, dc",
    "washington dc",
    "portland",
    "san diego",
    "san jose",
    "palo alto",
    "mountain view",
    "menlo park",
    "redwood city",
    "sunnyvale",
    "cupertino",
    "boulder",
    "raleigh",
    "durham",
    "nashville",
    "minneapolis",
    "detroit",
    "pittsburgh",
    "salt lake",
    "las vegas",
    "orlando",
    "tampa",
    "charlotte",
    "columbus",
    "indianapolis",
    "kansas city",
    "st. louis",
    "toronto",
    "vancouver",
    "london",
    "dublin",
    "berlin",
    "amsterdam",
    "paris",
    "tokyo",
    "singapore",
    "sydney",
    "bangalore",
    "bengaluru",
]

REMOTE_DISQUALIFIERS = [
    "hybrid",
    "on-site",
    "onsite",
    "on site",
    "in-office",
    "in office",
    "office required",
    "must be in office",
    "days in office",
    "days per week in the office",
    "come into the office",
    "relocation required",
    "must relocate",
    "willing to relocate",
    "relocate to",
    "commuting distance",
    "within commuting",
    "commute distance",
    "remote within commuting",
    "required office attendance",
    "office attendance required",
    "must live near",
    "local candidates only",
    "in-person required",
    "in person required",
]

# Stronger phrases only — scanned in description head (avoids culture/office mentions)
DESC_REMOTE_DISQUALIFIERS = [
    "hybrid required",
    "hybrid role",
    "this is a hybrid",
    "on-site required",
    "onsite required",
    "on site required",
    "must work from the office",
    "must be in office",
    "required to be in office",
    "3 days in office",
    "4 days in office",
    "5 days in office",
    "days per week in the office",
    "relocation required",
    "must relocate",
    "within commuting distance",
    "remote within commuting",
    "required office attendance",
    "must live near the office",
    "must be based near",
]

# Soft remote language that is NOT fully remote verification
SOFT_REMOTE_REJECT = [
    "remote-friendly",
    "remote friendly",
    "remotely friendly",
    "open to remote",
    "remote optional",
    "partially remote",
]

PRIORITY_REMOTE_COMPANIES = [
    "openai",
    "anthropic",
    "gitlab",
    "automattic",
    "zapier",
    "stripe",
    "datadog",
    "airtable",
    "hubspot",
    "canonical",
    "elastic",
    "docker",
    "cloudflare",
    "mozilla",
]

SENIOR_BLOCK = [
    "senior",
    "staff",
    "principal",
    "director",
    "vp ",
    "head of",
    "lead engineer",
    "10+ years",
    "8+ years",
    "7+ years",
    "6+ years",
]

YEARS_HARD_RE = re.compile(
    r"(?:at least|minimum of|min(?:imum)?\.?\s*|requires?\s+|must have\s+)?"
    r"(?:(\d+)\s*\+?\s*(?:-|to)\s*)?(\d+)\s*\+?\s*years?"
    r"(?:\s+of)?(?:\s+(?:professional|relevant|hands[- ]on))?\s+experience",
    re.I,
)

SOFTWARE_ENGINEER_HARD = [
    "software engineer",
    "full stack engineer",
    "fullstack engineer",
    "backend engineer",
    "frontend engineer",
    "sre ",
    "site reliability",
]


def load_profile() -> dict[str, Any]:
    return json.loads((TRUTH_DIR / "profile.json").read_text(encoding="utf-8"))


def load_portfolio() -> list[dict[str, Any]]:
    return json.loads((TRUTH_DIR / "portfolio_projects.json").read_text(encoding="utf-8"))


def load_master_resume() -> str:
    if MASTER_RESUME.exists():
        return MASTER_RESUME.read_text(encoding="utf-8")
    local = TRUTH_DIR / "master_resume.md"
    if local.exists():
        return local.read_text(encoding="utf-8")
    return ""


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def text_blob(job: dict[str, Any]) -> str:
    parts = [
        job.get("title", ""),
        job.get("company", ""),
        job.get("location", ""),
        job.get("description", ""),
        " ".join(job.get("tags", []) if isinstance(job.get("tags"), list) else [str(job.get("tags", ""))]),
    ]
    return normalize(" ".join(parts))


def is_remote(job: dict[str, Any]) -> bool:
    """Legacy helper — STRICT REMOTE MODE uses verify_remote() instead."""
    return verify_remote(job)["verified"]


def location_has_city(loc: str) -> bool:
    loc_n = normalize(loc)
    if not loc_n:
        return False
    if loc_n in REMOTE_LIKE_LOCATIONS:
        return False
    # Pure remote phrases without city
    if any(p in loc_n for p in VERIFIED_REMOTE_PHRASES) and not any(c in loc_n for c in CITY_MARKERS):
        return False
    return any(c in loc_n for c in CITY_MARKERS) or bool(
        re.search(r"\b[a-z]+,\s*[a-z]{2}\b", loc_n)  # City, ST pattern
    )


def has_verified_remote_phrase(text: str) -> bool:
    t = normalize(text)
    return any(p in t for p in VERIFIED_REMOTE_PHRASES)


def has_remote_disqualifier(text: str, *, description: bool = False) -> bool:
    t = normalize(text)
    phrases = DESC_REMOTE_DISQUALIFIERS if description else REMOTE_DISQUALIFIERS
    return any(d in t for d in phrases)


def verify_remote(job: dict[str, Any]) -> dict[str, Any]:
    """
    STRICT REMOTE MODE verification.
    Returns {verified: bool, label: str, reason: str}.
    Only Verified Remote jobs may appear in results.
    """
    loc = normalize(job.get("location", ""))
    title = normalize(job.get("title", ""))
    tags = job.get("tags") or []
    if isinstance(tags, list):
        tag_text = normalize(" ".join(str(t) for t in tags))
    else:
        tag_text = normalize(str(tags))
    desc_head = normalize(job.get("description", ""))[:1800]
    source = normalize(str(job.get("source", "")).split(":")[0])

    surface = f"{loc} {title} {tag_text}"

    if has_remote_disqualifier(surface) or has_remote_disqualifier(desc_head, description=True):
        return {
            "verified": False,
            "label": "✗ Not Verified Remote",
            "reason": "Disqualified: hybrid / on-site / office / relocation / commute language",
        }

    if any(s in surface or s in desc_head[:400] for s in SOFT_REMOTE_REJECT):
        # Soft language alone never verifies unless a hard allowlist phrase is also present
        if not has_verified_remote_phrase(surface) and not has_verified_remote_phrase(desc_head):
            return {
                "verified": False,
                "label": "✗ Not Verified Remote",
                "reason": "Remote-friendly / optional remote is not Fully Remote",
            }

    explicit = has_verified_remote_phrase(surface) or has_verified_remote_phrase(desc_head)
    city = location_has_city(job.get("location", ""))

    # City listed without explicit fully-remote phrase → reject
    if city and not explicit:
        return {
            "verified": False,
            "label": "✗ Not Verified Remote",
            "reason": "Location lists a city without an explicit Fully Remote / US Remote marker",
        }

    if explicit:
        if has_remote_disqualifier(loc) or any(s in loc for s in SOFT_REMOTE_REJECT):
            return {
                "verified": False,
                "label": "✗ Not Verified Remote",
                "reason": "Location still indicates hybrid/office/soft-remote requirement",
            }
        return {
            "verified": True,
            "label": "✓ Verified Remote",
            "reason": "Explicit fully remote / US remote / WFH marker found",
        }

    # Trusted remote boards: allow remote-like locations with no city
    if source in TRUSTED_REMOTE_SOURCES and not city:
        if loc in REMOTE_LIKE_LOCATIONS or (
            "remote" in loc and "friendly" not in loc and "optional" not in loc
        ):
            return {
                "verified": True,
                "label": "✓ Verified Remote",
                "reason": f"Trusted remote board ({source}) with non-city remote location",
            }

    # Plain location "Remote" / remote-like with no city (ATS boards)
    if not city and loc in REMOTE_LIKE_LOCATIONS:
        return {
            "verified": True,
            "label": "✓ Verified Remote",
            "reason": "Location explicitly Remote / US remote-like with no city",
        }
    if not city and loc.startswith("remote") and "friendly" not in loc and "optional" not in loc:
        return {
            "verified": True,
            "label": "✓ Verified Remote",
            "reason": "Location explicitly Remote / US remote-like with no city",
        }

    return {
        "verified": False,
        "label": "✗ Not Verified Remote",
        "reason": "No explicit Fully Remote / US Remote / 100% Remote / WFH verification",
    }


def is_fully_remote(job: dict[str, Any]) -> bool:
    """STRICT REMOTE MODE alias — only verified remote passes."""
    return verify_remote(job)["verified"]


def is_priority_remote_company(job: dict[str, Any]) -> bool:
    company = normalize(job.get("company", ""))
    source = normalize(job.get("source", ""))
    return any(c in company or c in source for c in PRIORITY_REMOTE_COMPANIES)


def is_us_friendly(job: dict[str, Any]) -> bool:
    blob = text_blob(job)
    loc = normalize(job.get("location", ""))

    blocked = [
        "india only",
        "eu only",
        "uk only",
        "emea only",
        "latam only",
        "canada only",
        "apac only",
    ]
    if any(b in blob for b in blocked):
        return False

    non_us_offices = [
        "tokyo",
        "seoul",
        "dublin",
        "london",
        "paris",
        "berlin",
        "amsterdam",
        "singapore",
        "sydney",
        "toronto",
        "vancouver",
        "bangalore",
        "bengaluru",
        "hyderabad",
        "mexico city",
        "mexico",
        "sao paulo",
        "tel aviv",
        "zurich",
        "ireland",
        "japan",
        "south korea",
        "united kingdom",
        "germany",
        "france",
        "netherlands",
        "australia",
        "india",
    ]
    loc_has_us = any(
        k in loc
        for k in [
            "united states",
            "usa",
            "u.s.",
            "remote-us",
            "remote us",
            "remote, us",
            "america",
            "california",
            "new york",
            "texas",
            "georgia",
            "colorado",
            "washington",
            "massachusetts",
            "illinois",
            "florida",
            "virginia",
            "oregon",
            "arizona",
            "utah",
            "pennsylvania",
            "ohio",
            "seattle",
            "atlanta",
            "chicago",
            "boston",
            "denver",
            "austin",
            "dallas",
            "miami",
            "los angeles",
            "san francisco",
            "sf,",
        ]
    ) or loc.strip() in {"usa", "us", "u.s.", "united states"}

    # Foreign office location is rejected unless location string also includes US/remote-US
    if any(x in loc for x in non_us_offices) and not loc_has_us:
        return False

    if loc_has_us or any(k in loc for k in US_KEYWORDS):
        return True
    if any(k in blob for k in ["remote-us", "remote us", "us remote", "united states", "usa only"]):
        return True
    if loc in {"", "worldwide", "anywhere", "global"} or loc == "remote":
        return True
    return False


def requires_five_plus_years(job: dict[str, Any]) -> bool:
    """True when JD hard-requires 5+ years (not merely preferred)."""
    blob = text_blob(job)
    hard_phrases = [
        "5+ years",
        "5 years of experience",
        "at least 5 years",
        "minimum 5 years",
        "6+ years",
        "7+ years",
        "8+ years",
        "10+ years",
    ]
    for phrase in hard_phrases:
        idx = blob.find(phrase)
        if idx == -1:
            continue
        window = blob[max(0, idx - 40) : idx + len(phrase) + 40]
        if "preferred" in window or "nice to have" in window or "bonus" in window:
            continue
        return True

    for match in YEARS_HARD_RE.finditer(blob):
        years = int(match.group(2))
        if years < 5:
            continue
        start, end = match.span()
        window = blob[max(0, start - 40) : end + 40]
        if "preferred" in window or "nice to have" in window or "bonus" in window:
            continue
        return True
    return False


QUICK_FILTERS: dict[str, list[str]] = {
    "AI Operations": ["ai operations", "ai ops", "ai operation"],
    "Workflow Automation": ["workflow automation", "workflow", "process automation", "automation"],
    "Technical Support": ["technical support", "support engineer", "product support", "support specialist"],
    "Solutions Engineer": ["solutions engineer", "solution engineer", "sales engineer", "demo engineer"],
    "Customer Success Engineer": ["customer success engineer", "customer success", "cs engineer"],
    "Customer Success": ["customer success", "customer success engineer", "cs associate"],
    "AI Implementation": ["ai implementation", "implementation specialist", "implementation engineer"],
    "Python": ["python"],
    "n8n": ["n8n"],
    "Airtable": ["airtable"],
    "OpenAI": ["openai", "chatgpt", "gpt-4", "gpt4"],
}


def requires_bachelors_hard(job: dict[str, Any]) -> bool:
    """True when a bachelor's (or higher) degree is a hard requirement."""
    blob = text_blob(job)
    degree_phrases = [
        "bachelor's degree required",
        "bachelors degree required",
        "bachelor degree required",
        "ba/bs required",
        "bs/ba required",
        "must have a bachelor",
        "requires a bachelor",
        "bachelor's degree is required",
        "degree required",
        "4-year degree required",
        "college degree required",
    ]
    for phrase in degree_phrases:
        idx = blob.find(phrase)
        if idx == -1:
            continue
        window = blob[max(0, idx - 50) : idx + len(phrase) + 50]
        if any(w in window for w in ["preferred", "nice to have", "bonus", "or equivalent", "equivalent experience"]):
            continue
        return True

    # "Bachelor's degree" near "required" without preferred
    if "bachelor" in blob:
        for m in re.finditer(r"bachelor", blob):
            window = blob[max(0, m.start() - 60) : m.end() + 80]
            if "required" in window and not any(
                w in window for w in ["preferred", "nice to have", "bonus", "or equivalent", "equivalent experience"]
            ):
                return True
    return False


def salary_mid(job: dict[str, Any]) -> float | None:
    smin = job.get("salary_min")
    smax = job.get("salary_max")
    if smin and smax:
        return (float(smin) + float(smax)) / 2
    if smin:
        return float(smin)
    if smax:
        return float(smax)
    return None


def meets_salary_floor(job: dict[str, Any], floor: float = 60000) -> bool:
    """
    Keep jobs at/above floor when salary is known.
    Unknown salary is kept (many boards omit pay) unless require_listed=True via caller.
    """
    mid = salary_mid(job)
    if mid is None:
        return True
    # Use max if available so a range like 55–75k can still pass
    smax = job.get("salary_max")
    if smax is not None and float(smax) >= floor:
        return True
    return mid >= floor


def matches_quick_filters(job: dict[str, Any], active: list[str] | None) -> bool:
    """OR semantics: job must match at least one active quick filter."""
    if not active:
        return True
    blob = text_blob(job)
    title = normalize(job.get("title", ""))
    for label in active:
        terms = QUICK_FILTERS.get(label) or [normalize(label)]
        if any(t in blob or t in title for t in terms):
            return True
    return False


def format_estimated_salary(job: dict[str, Any]) -> str:
    text = (job.get("salary_text") or "").strip()
    if text:
        return text
    smin = job.get("salary_min")
    smax = job.get("salary_max")
    if smin and smax and float(smin) != float(smax):
        return f"${float(smin):,.0f} – ${float(smax):,.0f}"
    if smin:
        return f"${float(smin):,.0f}+"
    if smax:
        return f"Up to ${float(smax):,.0f}"
    return "Not listed"


def is_honest_fit(job: dict[str, Any]) -> bool:
    """Reject roles that clearly exceed Leroy's verified experience profile."""
    title = normalize(job.get("title", ""))
    blob = text_blob(job)

    if any(t in title for t in SOFTWARE_ENGINEER_HARD):
        if not any(k in title for k in ["support", "solutions", "customer success", "implementation", "operations"]):
            return False

    if any(k in title for k in ["staff ", "principal ", "director", "vp ", "head of"]):
        return False

    # Manager roles are usually above current honest fit unless associate-level
    if "manager" in title and "associate" not in title:
        return False
    if "engineering manager" in title:
        return False

    coding_heavy = sum(
        1
        for k in ["python", "java ", "golang", "kubernetes", "terraform", "distributed systems"]
        if k in blob
    )
    ops_signals = sum(
        1
        for k in [
            "automation",
            "workflow",
            "support",
            "operations",
            "implementation",
            "no-code",
            "airtable",
            "n8n",
            "zapier",
        ]
        if k in blob
    )
    if coding_heavy >= 3 and ops_signals == 0:
        return False

    return True


def level_hint(job: dict[str, Any]) -> str:
    blob = text_blob(job)
    title = normalize(job.get("title", ""))
    if requires_five_plus_years(job):
        return "senior-leaning"
    if any(k in title for k in ["senior", "staff", "principal", "lead "]):
        return "senior-leaning"
    if any(k in blob for k in SENIOR_BLOCK) and not any(k in blob for k in LEVEL_KEYWORDS):
        return "senior-leaning"
    if any(k in blob for k in LEVEL_KEYWORDS) or any(k in title for k in ["junior", "associate", "entry"]):
        return "entry-junior-associate"
    return "mid-unspecified"


def role_match(job: dict[str, Any]) -> bool:
    title = normalize(job.get("title", ""))
    blob = text_blob(job)

    title_block = [
        "account executive",
        "sales executive",
        "growth marketer",
        "red team",
        "bug bounty",
        "product security",
        "security analyst",
        "risk analyst",
        "ai engineer",
        "genai engineer",
        "machine learning engineer",
        "data scientist",
        "recruiter",
        "recruiting",
        "penetration",
        "patient care",
        "influencer",
        "albertsons",
        "financial crimes",
        "biology",
        "events social",
        "chat support",
        "tax",
    ]
    if any(b in title for b in title_block):
        return False
    if " lead" in f" {title}" or title.startswith("lead "):
        return False

    if any(t in title for t in PRIORITY_TITLE_TERMS):
        return True

    title_ok = any(
        k in title
        for k in [
            "support",
            "operations",
            "automation",
            "implementation",
            "solutions",
            "customer success",
            "associate",
            "specialist",
            "workflow",
            "technical support",
            "ai operations",
            "ai support",
            "ops ",
            " process",
            "gtm operations",
            "demo engineer",
        ]
    )
    # Also allow pure remote board titles that are clearly ops/support/automation
    if any(k in title for k in ["no-code", "low-code", "zapier", "make.com", "n8n", "airtable"]):
        title_ok = True
    if not title_ok:
        return False
    hits = sum(1 for k in ROLE_KEYWORDS if k in blob)
    return hits >= 1


def priority_title_hit(job: dict[str, Any]) -> bool:
    title = normalize(job.get("title", ""))
    return any(t in title for t in PRIORITY_TITLE_TERMS)


def is_entry_level_friendly(job: dict[str, Any]) -> bool:
    hint = level_hint(job)
    if hint == "senior-leaning":
        return False
    title = normalize(job.get("title", ""))
    blob = text_blob(job)
    if any(k in title for k in LEVEL_KEYWORDS):
        return True
    if any(k in blob for k in LEVEL_KEYWORDS):
        return True
    # Mid-unspecified support/ops/automation titles stay eligible
    return hint == "mid-unspecified"


def should_keep(
    job: dict[str, Any],
    *,
    strict_level: bool = True,
    fully_remote_only: bool = True,
    us_only: bool = True,
    min_salary: float = 60000,
    prefer_no_degree: bool = True,
    block_five_plus_years: bool = True,
    quick_filters: list[str] | None = None,
    require_salary_listed: bool = False,
) -> bool:
    """STRICT REMOTE + PRODUCTION filters. Unverified remote / placeholders never pass."""
    from app.services.production import is_production_eligible

    ok, _reason = is_production_eligible(job)
    if not ok:
        return False

    verification = verify_remote(job)
    job["_remote_verification"] = verification
    if fully_remote_only:
        if not verification["verified"]:
            return False
    elif not is_remote(job):
        return False

    if us_only and not is_us_friendly(job):
        return False
    if not role_match(job):
        return False
    if not is_honest_fit(job):
        return False
    if block_five_plus_years and requires_five_plus_years(job):
        return False
    if not meets_salary_floor(job, min_salary):
        return False
    if require_salary_listed and salary_mid(job) is None and not (job.get("salary_text") or "").strip():
        return False
    # Prefer no bachelor's: soft-reject hard degree requirements when enabled
    if prefer_no_degree and requires_bachelors_hard(job):
        return False

    hint = level_hint(job)
    if strict_level:
        if not is_entry_level_friendly(job):
            return False
    if hint == "senior-leaning" and any(
        k in normalize(job.get("title", "")) for k in ["senior", "staff", "principal", "lead "]
    ):
        return False
    if not matches_quick_filters(job, quick_filters):
        return False
    return True


def parse_salary(text: str) -> tuple[float | None, float | None]:
    if not text:
        return None, None
    nums = [
        float(x.replace(",", ""))
        for x in re.findall(r"\$?\s?(\d{2,3}(?:,\d{3})+|\d{4,6})(?:k)?", text.lower())
    ]
    k_vals = [float(x) * 1000 for x in re.findall(r"(\d{2,3})\s?k", text.lower())]
    vals = nums + k_vals
    if not vals:
        return None, None
    if len(vals) == 1:
        return vals[0], vals[0]
    return min(vals), max(vals)


def match_reason(job: dict[str, Any], projects: list[dict[str, Any]]) -> str:
    """Truthful why-match using only JD overlap + verified portfolio/resume signals."""
    title = normalize(job.get("title", ""))
    blob = text_blob(job)
    profile = load_profile()
    parts: list[str] = []

    for term in PRIORITY_TITLE_TERMS:
        if term in title:
            parts.append(f"Title matches target role family ({term})")
            break

    tools = [t for t in ["n8n", "airtable", "openai", "python", "prompt", "workflow", "automation", "support", "qa"] if t in blob]
    resume_tools = [normalize(t) for t in profile.get("tools", [])]
    tool_overlap = [t for t in tools if t in resume_tools or t in {"workflow", "automation", "support", "prompt", "qa"}]
    if tool_overlap:
        parts.append("JD tools/skills overlap verified stack: " + ", ".join(tool_overlap[:5]))

    skill_hits = [normalize(s) for s in profile.get("skills", []) if normalize(s) in blob]
    if skill_hits:
        parts.append("Resume skills appear in JD: " + ", ".join(skill_hits[:4]))

    if any(k in blob for k in LEVEL_KEYWORDS):
        parts.append("Level language fits entry/junior/associate/specialist band")

    v = verify_remote(job)
    if v["verified"]:
        parts.append(v["label"])

    if projects:
        names = ", ".join(p["name"] for p in projects[:3])
        parts.append(f"Portfolio to reference: {names}")

    if not parts:
        parts.append("Limited verified overlap — review JD carefully before applying")
    return " · ".join(parts[:6])

