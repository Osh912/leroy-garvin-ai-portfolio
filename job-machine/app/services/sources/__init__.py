from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any

import httpx

from app.services.filters import parse_salary, verify_remote


def _id(source: str, raw: str) -> str:
    return hashlib.sha1(f"{source}:{raw}".encode()).hexdigest()[:16]


def _base(
    *,
    source: str,
    external_id: str,
    company: str,
    title: str,
    url: str,
    location: str,
    description: str,
    salary_text: str = "",
    tags: list[str] | None = None,
    posted_at: datetime | None = None,
) -> dict[str, Any]:
    smin, smax = parse_salary(salary_text)
    job = {
        "external_id": external_id or _id(source, url or f"{company}:{title}"),
        "source": source,
        "company": company.strip() or "Unknown",
        "title": title.strip() or "Untitled",
        "url": url,
        "location": location or "Remote",
        "description": description or "",
        "salary_text": salary_text or "",
        "salary_min": smin,
        "salary_max": smax,
        "tags": tags or [],
        "posted_at": posted_at,
        "is_remote": False,
    }
    verification = verify_remote(job)
    job["remote_verification"] = verification
    job["is_remote"] = bool(verification["verified"])
    job["remote_verified_label"] = verification["label"]
    return job


async def fetch_remoteok(client: httpx.AsyncClient) -> list[dict[str, Any]]:
    r = await client.get("https://remoteok.com/api", headers={"User-Agent": "LeroyJobMachine/1.0"})
    r.raise_for_status()
    data = r.json()
    out: list[dict[str, Any]] = []
    for row in data:
        if not isinstance(row, dict) or not row.get("id") or not row.get("position"):
            continue
        tags = row.get("tags") or []
        salary = ""
        if row.get("salary_min") or row.get("salary_max"):
            salary = f"${row.get('salary_min','')}-${row.get('salary_max','')}"
        out.append(
            _base(
                source="remoteok",
                external_id=str(row["id"]),
                company=str(row.get("company") or ""),
                title=str(row.get("position") or ""),
                url=str(row.get("url") or row.get("apply_url") or ""),
                location=str(row.get("location") or "Remote"),
                description=str(row.get("description") or ""),
                salary_text=salary,
                tags=[str(t) for t in tags],
            )
        )
    return out


async def fetch_remotive(client: httpx.AsyncClient) -> list[dict[str, Any]]:
    r = await client.get(
        "https://remotive.com/api/remote-jobs",
        params={"limit": 100},
        headers={"User-Agent": "LeroyJobMachine/1.0"},
    )
    r.raise_for_status()
    jobs = r.json().get("jobs", [])
    out: list[dict[str, Any]] = []
    for row in jobs:
        out.append(
            _base(
                source="remotive",
                external_id=str(row.get("id") or ""),
                company=str(row.get("company_name") or ""),
                title=str(row.get("title") or ""),
                url=str(row.get("url") or ""),
                location=str(row.get("candidate_required_location") or "Remote"),
                description=str(row.get("description") or ""),
                salary_text=str(row.get("salary") or ""),
                tags=list(row.get("tags") or []),
            )
        )
    return out


async def fetch_jobicy(client: httpx.AsyncClient) -> list[dict[str, Any]]:
    r = await client.get(
        "https://jobicy.com/api/v2/remote-jobs",
        params={"count": 50},
        headers={"User-Agent": "LeroyJobMachine/1.0"},
    )
    r.raise_for_status()
    jobs = r.json().get("jobs", [])
    out: list[dict[str, Any]] = []
    for row in jobs:
        out.append(
            _base(
                source="jobicy",
                external_id=str(row.get("id") or ""),
                company=str(row.get("companyName") or ""),
                title=str(row.get("jobTitle") or ""),
                url=str(row.get("url") or ""),
                location=str(row.get("jobGeo") or "Remote"),
                description=str(row.get("jobDescription") or ""),
                salary_text=str(row.get("annualSalaryMin") or "")
                + ("-" + str(row.get("annualSalaryMax")) if row.get("annualSalaryMax") else ""),
                tags=list(row.get("jobIndustry") or [])
                if isinstance(row.get("jobIndustry"), list)
                else [str(row.get("jobIndustry") or "")],
            )
        )
    return out


async def fetch_arbeitnow(client: httpx.AsyncClient) -> list[dict[str, Any]]:
    r = await client.get(
        "https://www.arbeitnow.com/api/job-board-api",
        headers={"User-Agent": "LeroyJobMachine/1.0"},
    )
    r.raise_for_status()
    jobs = r.json().get("data", [])
    out: list[dict[str, Any]] = []
    for row in jobs:
        out.append(
            _base(
                source="arbeitnow",
                external_id=str(row.get("slug") or row.get("url") or ""),
                company=str(row.get("company_name") or ""),
                title=str(row.get("title") or ""),
                url=str(row.get("url") or ""),
                location=str(row.get("location") or "Remote"),
                description=str(row.get("description") or ""),
                tags=list(row.get("tags") or []),
            )
        )
    return out


async def fetch_weworkremotely(client: httpx.AsyncClient) -> list[dict[str, Any]]:
    """We Work Remotely category RSS feeds (public)."""
    import re
    from xml.etree import ElementTree as ET

    feeds = [
        "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss",
        "https://weworkremotely.com/categories/remote-customer-support-jobs.rss",
        "https://weworkremotely.com/categories/remote-product-jobs.rss",
        "https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss",
    ]
    out: list[dict[str, Any]] = []
    for feed in feeds:
        try:
            r = await client.get(feed, headers={"User-Agent": "LeroyJobMachine/1.0"})
            if r.status_code >= 400:
                continue
            root = ET.fromstring(r.text)
            for item in root.findall(".//item"):
                title = (item.findtext("title") or "").strip()
                link = (item.findtext("link") or "").strip()
                desc_raw = item.findtext("description") or ""
                desc = re.sub(r"<[^>]+>", " ", desc_raw)
                desc = re.sub(r"\s+", " ", desc).strip()
                company = ""
                role = title
                if ":" in title:
                    company, role = [p.strip() for p in title.split(":", 1)]
                # Prefer region text from WWR markup when present
                region = ""
                m_region = re.search(
                    r'class="[^"]*region[^"]*"[^>]*>([^<]+)',
                    desc_raw,
                    re.I,
                )
                if m_region:
                    region = m_region.group(1).strip()
                if not region:
                    m_loc = re.search(
                        r"\b((?:Fully\s+)?Remote(?:\s*[-–—,]?\s*(?:United States|USA|US|Only))?|Work From Home|100%\s*Remote)\b",
                        desc,
                        re.I,
                    )
                    region = m_loc.group(1).strip() if m_loc else "Remote - United States"
                # Guard against broken HTML leftovers
                if "imgix" in region.lower() or "http" in region.lower() or len(region) > 80:
                    region = "Remote - United States"
                out.append(
                    _base(
                        source="weworkremotely",
                        external_id=_id("wwr", link or title),
                        company=company or "Unknown",
                        title=role or title,
                        url=link,
                        location=region,
                        description=desc,
                        tags=["remote", "weworkremotely", "fully remote"],
                    )
                )
        except Exception:  # noqa: BLE001
            continue
    return out


async def fetch_greenhouse_board(client: httpx.AsyncClient, board: str) -> list[dict[str, Any]]:
    r = await client.get(
        f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs",
        params={"content": "true"},
        headers={"User-Agent": "LeroyJobMachine/1.0"},
    )
    if r.status_code >= 400:
        return []
    jobs = r.json().get("jobs", [])
    out: list[dict[str, Any]] = []
    for row in jobs:
        loc = ""
        if isinstance(row.get("location"), dict):
            loc = str(row["location"].get("name") or "")
        if not loc and isinstance(row.get("offices"), list):
            loc = ", ".join(o.get("name", "") for o in row["offices"] if isinstance(o, dict))
        out.append(
            _base(
                source=f"greenhouse:{board}",
                external_id=str(row.get("id") or ""),
                company=board,
                title=str(row.get("title") or ""),
                url=str(row.get("absolute_url") or ""),
                location=loc or "Remote",
                description=str(row.get("content") or ""),
            )
        )
    return out


async def fetch_lever_company(client: httpx.AsyncClient, company: str) -> list[dict[str, Any]]:
    r = await client.get(
        f"https://api.lever.co/v0/postings/{company}",
        params={"mode": "json"},
        headers={"User-Agent": "LeroyJobMachine/1.0"},
    )
    if r.status_code >= 400:
        return []
    jobs = r.json()
    out: list[dict[str, Any]] = []
    for row in jobs:
        cats = row.get("categories") or {}
        out.append(
            _base(
                source=f"lever:{company}",
                external_id=str(row.get("id") or ""),
                company=company,
                title=str(row.get("text") or ""),
                url=str(row.get("hostedUrl") or row.get("applyUrl") or ""),
                location=str(cats.get("location") or "Remote"),
                description=str(row.get("descriptionPlain") or row.get("description") or ""),
                tags=[str(cats.get("team") or ""), str(cats.get("commitment") or "")],
            )
        )
    return out


async def fetch_ashby_board(client: httpx.AsyncClient, board: str) -> list[dict[str, Any]]:
    # Ashby public job board API
    r = await client.get(
        f"https://api.ashbyhq.com/posting-api/job-board/{board}",
        headers={"User-Agent": "LeroyJobMachine/1.0"},
    )
    if r.status_code >= 400:
        return []
    jobs = r.json().get("jobs", [])
    out: list[dict[str, Any]] = []
    for row in jobs:
        out.append(
            _base(
                source=f"ashby:{board}",
                external_id=str(row.get("id") or row.get("jobUrl") or ""),
                company=board,
                title=str(row.get("title") or ""),
                url=str(row.get("jobUrl") or ""),
                location=str(row.get("location") or "Remote"),
                description=str(row.get("descriptionPlain") or row.get("descriptionHtml") or ""),
            )
        )
    return out


async def fetch_workable_company(client: httpx.AsyncClient, company: str) -> list[dict[str, Any]]:
    """Workable public careers widget API (rate-limit aware)."""
    r = await client.get(
        f"https://apply.workable.com/api/v1/widget/accounts/{company}",
        headers={"User-Agent": "LeroyJobMachine/1.0"},
    )
    if r.status_code == 429:
        raise RuntimeError(f"workable:{company} rate limited")
    if r.status_code >= 400:
        return []
    jobs = r.json().get("jobs", []) if isinstance(r.json(), dict) else []
    out: list[dict[str, Any]] = []
    for row in jobs:
        loc = row.get("location") or {}
        loc_str = ""
        if isinstance(loc, dict):
            loc_str = ", ".join(
                str(x) for x in [loc.get("city"), loc.get("region"), loc.get("country")] if x
            )
        elif isinstance(loc, str):
            loc_str = loc
        tele = row.get("telecommuting") or row.get("remote")
        if tele:
            loc_str = (loc_str + " Remote").strip()
        out.append(
            _base(
                source=f"workable:{company}",
                external_id=str(row.get("shortcode") or row.get("id") or ""),
                company=str(row.get("company") or company),
                title=str(row.get("title") or ""),
                url=str(row.get("url") or row.get("shortlink") or ""),
                location=loc_str or ("Remote" if tele else "Unknown"),
                description=str(row.get("description") or ""),
                tags=["workable", "remote"] if tele else ["workable"],
            )
        )
    return out


async def fetch_with_retry(coro_factory, *, attempts: int = 2, label: str = "source"):
    """Retry failed sources once (rate limits / transient errors)."""
    last_exc: Exception | None = None
    for i in range(attempts):
        try:
            return await coro_factory()
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if i + 1 < attempts:
                import asyncio

                await asyncio.sleep(0.6 * (i + 1))
    raise RuntimeError(f"{label} failed after {attempts} attempts: {last_exc}")
