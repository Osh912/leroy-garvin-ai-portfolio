#!/usr/bin/env python3
"""SMART JOB RANKING — fetch, filter, rank, save top 10 (no auto-apply)."""

from __future__ import annotations

import asyncio
import json
from datetime import date, datetime
from pathlib import Path

from app.database import SessionLocal, init_db
from app.models import Application, Job
from app.services.job_finder import purge_unverified_remote, search_jobs, upsert_jobs
from app.services.resume_tailor import tailor_resume
from app.services.cover_letter import generate_cover_letter

OUT = Path(__file__).resolve().parents[1] / "data" / "live_top10.json"


async def run() -> dict:
    init_db()
    result = await search_jobs(
        strict_level=True,
        fully_remote_only=True,
        us_only=True,
        min_salary=60000,
        prefer_no_degree=True,
        block_five_plus_years=True,
    )
    db = SessionLocal()
    try:
        purged = purge_unverified_remote(db)
        upsert_jobs(db, result["jobs"])

        # Re-load from DB with scores, prefer priority-ranked list from search result
        top = result["jobs"][:10]

        # Map external ids to DB rows
        saved_apps = []
        report_rows = []
        for rank, job in enumerate(top, start=1):
            row = (
                db.query(Job)
                .filter(Job.source == job["source"], Job.external_id == job["external_id"])
                .one_or_none()
            )
            if not row:
                continue

            projects = job.get("matched_projects") or []
            why = job.get("match_reason") or (job.get("score_breakdown") or {}).get("why_match", "")
            interview = float((job.get("score_breakdown") or {}).get("interview_probability") or 0)
            est_salary = job.get("estimated_salary") or row.salary_text or "Not listed"

            # Generate truthful packet (template unless OpenAI key set)
            resume, _, _ = tailor_resume(job, projects)
            cover, _, _ = generate_cover_letter(job, projects)

            existing = (
                db.query(Application)
                .filter(Application.job_id == row.id, Application.status == "saved")
                .one_or_none()
            )
            if existing:
                existing.application_score = float(job.get("score") or 0)
                existing.portfolio_refs = json.dumps(projects)
                existing.tailored_resume = resume
                existing.cover_letter = cover
                existing.notes = f"[Live search rank #{rank}] {why}"
                existing.updated_at = datetime.utcnow()
                app_row = existing
            else:
                app_row = Application(
                    job_id=row.id,
                    company=row.company,
                    position=row.title,
                    salary=row.salary_text or "",
                    location=row.location,
                    date_applied=None,  # not applied — awaiting approval
                    status="saved",
                    follow_up_date=None,
                    interview_date=None,
                    notes=f"[Live search rank #{rank}] {why}",
                    recruiter_name="",
                    recruiter_email="",
                    tailored_resume=resume,
                    cover_letter=cover,
                    portfolio_refs=json.dumps(projects),
                    application_score=float(job.get("score") or 0),
                )
                db.add(app_row)

            row.status = "saved"
            db.commit()
            db.refresh(app_row)

            saved_apps.append(app_row.id)
            report_rows.append(
                {
                    "rank": rank,
                    "job_id": row.id,
                    "application_id": app_row.id,
                    "company": row.company,
                    "title": row.title,
                    "estimated_salary": est_salary,
                    "salary": est_salary,
                    "location": row.location,
                    "url": row.url,
                    "source": row.source,
                    "remote_verified": True,
                    "remote_verified_label": "✓ Verified Remote",
                    "match_percentage": float(job.get("score") or 0),
                    "score": float(job.get("score") or 0),
                    "interview_probability": interview,
                    "score_breakdown": job.get("score_breakdown") or {},
                    "why_match": why,
                    "projects": [
                        {"name": p.get("name"), "url": p.get("url")} for p in projects[:4]
                    ],
                    "status": "saved",
                    "auto_submitted": False,
                }
            )

        # Dashboard snapshot
        today = date.today()
        start = datetime(today.year, today.month, today.day)
        apps = db.query(Application).all()
        dashboard = {
            "new_jobs": db.query(Job).filter(Job.found_at >= start).count(),
            "highest_match_jobs": len(report_rows),
            "applications_sent": sum(1 for a in apps if a.status in {"applied", "interview", "offer"}),
            "follow_ups_due": sum(
                1
                for a in apps
                if a.follow_up_date
                and a.follow_up_date <= today
                and a.status not in {"rejected", "offer", "withdrawn"}
            ),
            "interviews": sum(1 for a in apps if a.status == "interview" or a.interview_date),
            "saved_awaiting_approval": sum(1 for a in apps if a.status == "saved"),
        }

        payload = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "ranking_mode": "smart+strict-remote",
            "remote_mode": "strict",
            "purged_unverified_remote": purged,
            "rejected_unverified_remote": result.get("rejected_unverified_remote", 0),
            "weights": result.get("weights"),
            "filters_applied": result.get("filters_applied"),
            "fetched": result["fetched"],
            "matched": result["matched"],
            "errors": result["errors"],
            "sources_note": result["sources_note"],
            "dashboard": dashboard,
            "top_10": report_rows,
            "auto_apply": False,
            "open_ui": "http://127.0.0.1:8787",
        }
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return payload
    finally:
        db.close()


if __name__ == "__main__":
    data = asyncio.run(run())
    print(json.dumps({
        "fetched": data["fetched"],
        "matched": data["matched"],
        "top": len(data["top_10"]),
        "dashboard": data["dashboard"],
        "out": str(OUT),
    }, indent=2))
