from __future__ import annotations

"""Verify job postings are still active via HTTP checks."""

import asyncio
from datetime import datetime
from typing import Any

import httpx

INACTIVE_MARKERS = [
    "no longer accepting applications",
    "this job is no longer available",
    "position has been filled",
    "job not found",
    "page not found",
    "404",
    "this posting is closed",
    "requisition is closed",
    "sorry, this job",
    "opening is closed",
]


async def check_posting_active(
    client: httpx.AsyncClient,
    url: str,
) -> dict[str, Any]:
    """
    Return {active: bool, status_code: int|None, reason: str, checked_at: iso}.
    Conservative: network errors keep the job (unknown) rather than inventing closure.
    Explicit 404/410 or closed-page markers mark inactive.
    """
    checked_at = datetime.utcnow().isoformat() + "Z"
    if not url:
        return {"active": False, "status_code": None, "reason": "missing_url", "checked_at": checked_at}

    try:
        r = await client.head(url, follow_redirects=True)
        code = r.status_code
        # Some boards block HEAD — fall through to GET
        if code in {405, 403, 501}:
            r = await client.get(url, follow_redirects=True)
            code = r.status_code
        elif code >= 400:
            r = await client.get(url, follow_redirects=True)
            code = r.status_code
    except Exception as exc:  # noqa: BLE001
        return {
            "active": True,  # do not invent closure on network failure
            "status_code": None,
            "reason": f"check_error_kept:{type(exc).__name__}",
            "checked_at": checked_at,
            "unknown": True,
        }

    if code in {404, 410, 451}:
        return {"active": False, "status_code": code, "reason": f"http_{code}", "checked_at": checked_at}

    if code >= 500:
        return {
            "active": True,
            "status_code": code,
            "reason": f"server_error_kept:{code}",
            "checked_at": checked_at,
            "unknown": True,
        }

    body = ""
    try:
        if r.request.method != "HEAD":
            body = (r.text or "")[:8000].lower()
    except Exception:  # noqa: BLE001
        body = ""

    for marker in INACTIVE_MARKERS:
        if marker in body:
            return {
                "active": False,
                "status_code": code,
                "reason": f"marker:{marker}",
                "checked_at": checked_at,
            }

    return {"active": True, "status_code": code, "reason": "ok", "checked_at": checked_at}


async def verify_jobs_active(jobs: list[dict[str, Any]], *, concurrency: int = 8) -> list[dict[str, Any]]:
    """Annotate jobs with active_check; drop inactive ones from returned list."""
    sem = asyncio.Semaphore(concurrency)
    out: list[dict[str, Any]] = []

    async with httpx.AsyncClient(
        timeout=12.0,
        follow_redirects=True,
        headers={"User-Agent": "LeroyJobMachine/2.0 (+production-active-check)"},
    ) as client:

        async def one(job: dict[str, Any]) -> dict[str, Any] | None:
            async with sem:
                result = await check_posting_active(client, str(job.get("url") or ""))
            job = dict(job)
            job["active_check"] = result
            job["is_active"] = bool(result.get("active"))
            job["last_verified_at"] = result.get("checked_at")
            if not job["is_active"]:
                return None
            return job

        checked = await asyncio.gather(*(one(j) for j in jobs))
        out = [j for j in checked if j is not None]
    return out
