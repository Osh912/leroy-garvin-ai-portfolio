from __future__ import annotations

"""
Recruiter Analytics — computed only from tracked Application history.
Never invents companies, applications, interviews, offers, or statistics.
"""

import csv
import io
import json
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from app.models import Application, Job
from app.services.filters import normalize, parse_salary
from app.services.pipeline_stages import (
    APPLIED_OR_LATER,
    INTERVIEW_STAGES,
    REPLY_STAGES,
    normalize_status,
    stage_label,
)


def _parse_meta(row: Application) -> dict[str, Any]:
    raw = getattr(row, "analytics_json", None) or "{}"
    try:
        data = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except json.JSONDecodeError:
        data = {}
    return data if isinstance(data, dict) else {}


def _salary_mid(text: str, job: Job | None = None) -> float | None:
    if job and (job.salary_min or job.salary_max):
        if job.salary_min and job.salary_max:
            return (float(job.salary_min) + float(job.salary_max)) / 2
        return float(job.salary_min or job.salary_max)
    smin, smax = parse_salary(text or "")
    if smin and smax:
        return (smin + smax) / 2
    return smin or smax


def _role_bucket(title: str) -> str:
    t = normalize(title)
    buckets = [
        ("ai operations", "AI Operations"),
        ("workflow automation", "Workflow Automation"),
        ("automation specialist", "Automation Specialist"),
        ("technical support", "Technical Support"),
        ("support engineer", "Technical Support"),
        ("support specialist", "Technical Support"),
        ("solutions engineer", "Solutions Engineer"),
        ("customer success", "Customer Success"),
        ("ai implementation", "AI Implementation"),
        ("implementation", "AI Implementation"),
        ("devops", "DevOps / Infra"),
    ]
    for key, label in buckets:
        if key in t:
            return label
    return "Other"


def _days_between(a: date | datetime | None, b: date | datetime | None) -> float | None:
    if not a or not b:
        return None
    if isinstance(a, datetime):
        a = a.date()
    if isinstance(b, datetime):
        b = b.date()
    return float((b - a).days)


def _avg(nums: list[float]) -> float | None:
    if not nums:
        return None
    return round(sum(nums) / len(nums), 1)


def _pct(num: int, den: int) -> float | None:
    if den <= 0:
        return None
    return round(100.0 * num / den, 1)


def load_applications(db: Session) -> list[Application]:
    return db.query(Application).order_by(Application.created_at.desc()).all()


def build_kpis(apps: list[Application], db: Session) -> dict[str, Any]:
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    applied = [a for a in apps if normalize_status(a.status) in APPLIED_OR_LATER or a.date_applied]
    submitted_today = sum(1 for a in applied if a.date_applied == today)
    submitted_week = sum(1 for a in applied if a.date_applied and a.date_applied >= week_start)
    submitted_month = sum(1 for a in applied if a.date_applied and a.date_applied >= month_start)

    replies = [a for a in apps if normalize_status(a.status) in REPLY_STAGES or normalize_status(a.status) in {
        "phone_screen", "technical_interview", "hiring_manager", "final_interview", "offer", "accepted"
    }]
    # Recruiter replies = any stage past applied that indicates human response (not just viewed)
    recruiter_replies = [
        a
        for a in apps
        if normalize_status(a.status)
        in {
            "recruiter_replied",
            "phone_screen",
            "technical_interview",
            "hiring_manager",
            "final_interview",
            "offer",
            "accepted",
        }
        or (normalize_status(a.status) == "recruiter_contact")
    ]
    recruiter_screens = [a for a in apps if normalize_status(a.status) == "phone_screen"]
    tech = [a for a in apps if normalize_status(a.status) == "technical_interview"]
    final = [a for a in apps if normalize_status(a.status) == "final_interview"]
    offers = [a for a in apps if normalize_status(a.status) in {"offer", "accepted"}]
    rejected = [a for a in apps if normalize_status(a.status) == "rejected"]
    interviews = [
        a
        for a in apps
        if is_interview_like(a) or a.interview_date
    ]

    applied_count = sum(1 for a in apps if a.date_applied or normalize_status(a.status) in APPLIED_OR_LATER)
    # Ghosted: applied 14+ days ago, no reply stages, not rejected/withdrawn/offer
    ghosted = []
    for a in apps:
        st = normalize_status(a.status)
        if st in {"rejected", "withdrawn", "offer", "accepted"}:
            continue
        if not a.date_applied:
            continue
        if (today - a.date_applied).days < 14:
            continue
        if st in REPLY_STAGES or st in {"phone_screen", "technical_interview", "hiring_manager", "final_interview"}:
            continue
        if st in {"applied", "recruiter_viewed"}:
            ghosted.append(a)

    follow_ups_due = sum(
        1
        for a in apps
        if a.follow_up_date
        and a.follow_up_date <= today
        and normalize_status(a.status) not in {"rejected", "offer", "accepted", "withdrawn"}
    )

    response_days: list[float] = []
    interview_days: list[float] = []
    for a in apps:
        meta = _parse_meta(a)
        applied_on = a.date_applied
        replied_on = meta.get("first_response_date")
        if replied_on:
            try:
                rd = date.fromisoformat(str(replied_on)[:10])
                d = _days_between(applied_on, rd)
                if d is not None and d >= 0:
                    response_days.append(d)
            except ValueError:
                pass
        if a.interview_date and applied_on:
            d = _days_between(applied_on, a.interview_date)
            if d is not None and d >= 0:
                interview_days.append(d)

    resume_downloads = 0
    for a in apps:
        meta = _parse_meta(a)
        resume_downloads += int(meta.get("resume_download_count") or 0)

    return {
        "applications_submitted_today": submitted_today,
        "applications_this_week": submitted_week,
        "applications_this_month": submitted_month,
        "applications_total_applied": applied_count,
        "recruiter_replies": len(recruiter_replies),
        "recruiter_response_rate": _pct(len(recruiter_replies), applied_count),
        "interview_invitations": len(interviews),
        "recruiter_screens": len(recruiter_screens),
        "technical_interviews": len(tech),
        "final_interviews": len(final),
        "job_offers": len(offers),
        "rejections": len(rejected),
        "ghosted_applications": len(ghosted),
        "follow_ups_due": follow_ups_due,
        "average_days_until_response": _avg(response_days),
        "average_days_until_interview": _avg(interview_days),
        "offer_rate": _pct(len(offers), applied_count),
        "interview_rate": _pct(len(interviews), applied_count),
        "resume_download_count": resume_downloads if resume_downloads else None,
        "data_note": "All KPIs computed from tracked applications only. Null rates mean insufficient applied history.",
    }


def is_interview_like(a: Application) -> bool:
    st = normalize_status(a.status)
    return st in INTERVIEW_STAGES or st in {
        "phone_screen",
        "technical_interview",
        "hiring_manager",
        "final_interview",
    }


def build_success_metrics(apps: list[Application], db: Session) -> dict[str, Any]:
    jobs = {j.id: j for j in db.query(Job).all()}

    resume_stats: dict[str, Counter] = defaultdict(Counter)
    cover_stats: dict[str, Counter] = defaultdict(Counter)
    company_reply: Counter = Counter()
    company_applied: Counter = Counter()
    company_interview: Counter = Counter()
    company_salary_interview: dict[str, list[float]] = defaultdict(list)
    company_salary_offer: dict[str, list[float]] = defaultdict(list)
    recruiter_reply: Counter = Counter()
    fastest: list[dict[str, Any]] = []
    interview_sals: list[float] = []
    offer_sals: list[float] = []

    for a in apps:
        meta = _parse_meta(a)
        st = normalize_status(a.status)
        rv = meta.get("resume_version") or "default"
        cv = meta.get("cover_version") or "default"
        resume_stats[rv]["total"] += 1
        cover_stats[cv]["total"] += 1
        if st in REPLY_STAGES or st in {"phone_screen", "technical_interview", "hiring_manager", "final_interview", "offer", "accepted"}:
            resume_stats[rv]["replies"] += 1
            cover_stats[cv]["replies"] += 1

        if a.date_applied or st in APPLIED_OR_LATER:
            company_applied[a.company] += 1
        if st in {
            "recruiter_replied",
            "phone_screen",
            "technical_interview",
            "hiring_manager",
            "final_interview",
            "offer",
            "accepted",
        } or a.status == "recruiter_contact":
            company_reply[a.company] += 1
            if a.recruiter_name:
                recruiter_reply[a.recruiter_name] += 1

        job = jobs.get(a.job_id)
        sal = _salary_mid(a.salary, job)
        if is_interview_like(a) or a.interview_date:
            company_interview[a.company] += 1
            if sal:
                interview_sals.append(sal)
                company_salary_interview[a.company].append(sal)
            # fastest interview response
            d = _days_between(a.date_applied, a.interview_date)
            if d is not None:
                fastest.append({"company": a.company, "position": a.position, "days": d})

        if st in {"offer", "accepted"} and sal:
            offer_sals.append(sal)
            company_salary_offer[a.company].append(sal)

    def best_version(stats: dict[str, Counter]) -> dict[str, Any] | None:
        best = None
        best_rate = -1.0
        for ver, c in stats.items():
            total = c["total"]
            if total < 1:
                continue
            rate = c["replies"] / total
            if rate > best_rate:
                best_rate = rate
                best = {
                    "version": ver,
                    "applications": total,
                    "replies": c["replies"],
                    "reply_rate": _pct(c["replies"], total),
                }
        return best

    def top_companies(counter: Counter, applied: Counter | None = None, limit: int = 5) -> list[dict[str, Any]]:
        rows = []
        for company, n in counter.most_common(20):
            base = applied[company] if applied is not None else n
            rows.append(
                {
                    "company": company,
                    "count": n,
                    "applied": base if applied is not None else None,
                    "rate": _pct(n, base) if applied is not None else None,
                }
            )
        # Prefer rate when enough volume
        if applied is not None:
            rows = [r for r in rows if (r["applied"] or 0) >= 1]
            rows.sort(key=lambda r: (r["rate"] or 0, r["count"]), reverse=True)
        return rows[:limit]

    fastest_sorted = sorted(fastest, key=lambda x: x["days"])[:5]
    highest_salary_companies = sorted(
        (
            {"company": c, "average_salary": _avg(v), "samples": len(v)}
            for c, v in company_salary_interview.items()
            if v
        ),
        key=lambda x: x["average_salary"] or 0,
        reverse=True,
    )[:5]

    return {
        "best_performing_resume_version": best_version(resume_stats),
        "best_performing_cover_letter": best_version(cover_stats),
        "highest_response_companies": top_companies(company_reply, company_applied),
        "highest_interview_companies": top_companies(company_interview, company_applied),
        "highest_salary_companies": highest_salary_companies,
        "most_responsive_recruiters": [
            {"recruiter": name, "replies": n} for name, n in recruiter_reply.most_common(5)
        ],
        "fastest_interview_response": fastest_sorted,
        "average_salary_of_interviews": _avg(interview_sals),
        "average_salary_of_offers": _avg(offer_sals),
        "insufficient_data": len(apps) == 0,
    }


def build_insights(apps: list[Application], kpis: dict[str, Any], success: dict[str, Any]) -> list[str]:
    """Generate insights only when real counts support them. Never invent."""
    insights: list[str] = []
    if not apps:
        return [
            "No tracked applications yet. Insights appear after you mark applications Applied and update stages."
        ]

    # Role interview rates
    role_applied: Counter = Counter()
    role_interview: Counter = Counter()
    weekday_applied: Counter = Counter()
    for a in apps:
        role = _role_bucket(a.position)
        st = normalize_status(a.status)
        if a.date_applied or st in APPLIED_OR_LATER:
            role_applied[role] += 1
            if a.date_applied:
                weekday_applied[a.date_applied.strftime("%A")] += 1
        if is_interview_like(a) or a.interview_date:
            role_interview[role] += 1

    rates = []
    for role, n in role_applied.items():
        if n >= 2:
            rates.append((role, role_interview[role] / n, n, role_interview[role]))
    rates.sort(key=lambda x: x[1], reverse=True)
    if len(rates) >= 2 and rates[0][1] > 0 and rates[1][1] > 0:
        if rates[0][1] >= rates[1][1] * 1.5:
            insights.append(
                f"{rates[0][0]} roles are producing interviews at a higher rate "
                f"({_pct(rates[0][3], rates[0][2])}% of {rates[0][2]} apps) than {rates[1][0]} "
                f"({_pct(rates[1][3], rates[1][2])}% of {rates[1][2]} apps)."
            )
    elif rates and rates[0][3] > 0:
        insights.append(
            f"{rates[0][0]} currently leads interview conversion "
            f"({rates[0][3]} interview(s) from {rates[0][2]} applied)."
        )

    top_resp = (success.get("highest_response_companies") or [])[:1]
    if top_resp and top_resp[0].get("rate") is not None and (top_resp[0].get("applied") or 0) >= 1:
        insights.append(
            f"{top_resp[0]['company']} has the highest tracked response rate "
            f"({top_resp[0]['rate']}% — {top_resp[0]['count']} replies / {top_resp[0]['applied']} applied)."
        )

    if weekday_applied:
        best_day, n = weekday_applied.most_common(1)[0]
        if n >= 2:
            insights.append(
                f"Most tracked applications were submitted on {best_day}s ({n} applications). "
                "Compare reply rates as more data accumulates."
            )

    resume = success.get("best_performing_resume_version")
    if resume and (resume.get("applications") or 0) >= 2 and resume.get("reply_rate") is not None:
        insights.append(
            f"Resume version “{resume['version']}” has the best tracked reply rate "
            f"({resume['reply_rate']}% across {resume['applications']} applications)."
        )

    if kpis.get("ghosted_applications"):
        insights.append(
            f"{kpis['ghosted_applications']} application(s) look ghosted (applied ≥14 days ago with no reply stage)."
        )

    if kpis.get("follow_ups_due"):
        insights.append(f"{kpis['follow_ups_due']} follow-up(s) are due — review the Follow-up Engine.")

    if not insights:
        insights.append(
            f"Tracking {len(apps)} application(s). Insights unlock as stages move past Applied "
            "(replies, screens, interviews)."
        )
    return insights


def build_followups(apps: list[Application]) -> list[dict[str, Any]]:
    today = date.today()
    out: list[dict[str, Any]] = []
    for a in apps:
        st = normalize_status(a.status)
        if st in {"rejected", "withdrawn", "offer", "accepted"}:
            continue
        if not a.date_applied:
            continue
        days = (today - a.date_applied).days
        cadence = None
        if days >= 14:
            cadence = 14
        elif days >= 7:
            cadence = 7
        elif days >= 3:
            cadence = 3
        if cadence is None:
            continue
        # Skip if already in active interview loop
        if is_interview_like(a):
            continue
        meta = _parse_meta(a)
        approved = meta.get("followup_approvals") or {}
        cadence_key = str(cadence)
        already = isinstance(approved, dict) and approved.get(cadence_key)
        email = _followup_email(a, cadence)
        out.append(
            {
                "application_id": a.id,
                "company": a.company,
                "position": a.position,
                "date_applied": a.date_applied.isoformat(),
                "days_since_application": days,
                "recommended_cadence_days": cadence,
                "recruiter_name": a.recruiter_name or "",
                "recruiter_email": a.recruiter_email or "",
                "subject": email["subject"],
                "body": email["body"],
                "approval_required": True,
                "auto_send": False,
                "status": "approved_not_sent" if already else "pending_approval",
                "approved_at": already.get("approved_at") if isinstance(already, dict) else None,
                "sent": False,
            }
        )
    out.sort(key=lambda x: (-x["days_since_application"], x["company"]))
    return out


def approve_followup(db: Session, application_id: int, cadence_days: int) -> dict[str, Any]:
    """Record Leroy's approval to send a follow-up. Never sends email automatically."""
    row = db.get(Application, application_id)
    if not row:
        raise ValueError("Application not found")
    meta = _parse_meta(row)
    approvals = meta.get("followup_approvals") or {}
    if not isinstance(approvals, dict):
        approvals = {}
    approvals[str(cadence_days)] = {
        "approved_at": datetime.utcnow().isoformat() + "Z",
        "cadence_days": cadence_days,
        "auto_send": False,
        "sent": False,
        "note": "Approved for Leroy to send manually — Job Machine never auto-sends.",
    }
    meta["followup_approvals"] = approvals
    row.analytics_json = json.dumps(meta)
    if not row.follow_up_date or row.follow_up_date <= date.today():
        row.follow_up_date = date.today() + timedelta(days=max(1, 7 - (cadence_days % 7)))
    db.add(row)
    db.commit()
    db.refresh(row)
    email = _followup_email(row, cadence_days)
    return {
        "application_id": row.id,
        "company": row.company,
        "position": row.position,
        "cadence_days": cadence_days,
        "approved": True,
        "sent": False,
        "auto_send": False,
        "subject": email["subject"],
        "body": email["body"],
        "recruiter_email": row.recruiter_email or "",
        "message": "Follow-up approved. Copy and send manually — nothing was emailed.",
    }


def _followup_email(a: Application, cadence: int) -> dict[str, str]:
    name = a.recruiter_name.strip() if a.recruiter_name else "Hiring Team"
    subject = f"Following up — {a.position} at {a.company}"
    body = f"""Hi {name},

I wanted to politely follow up on my application for the {a.position} role at {a.company} (submitted about {cadence}+ days ago).

I remain very interested in contributing to remote AI Operations / Workflow Automation / Technical Support work and can share portfolio evidence here:
https://leroy-garvin-ai-portfolio.vercel.app

Happy to provide any additional materials. Thank you for your time.

Best regards,
Leroy Garvin Jr
AlignedVibesCo@gmail.com
(912) 901-6378
"""
    return {"subject": subject, "body": body.strip()}


def build_interview_analytics(apps: list[Application]) -> dict[str, Any]:
    behavioral_pass = 0
    behavioral_total = 0
    technical_pass = 0
    technical_total = 0
    questions: Counter = Counter()
    weak: Counter = Counter()
    strong: Counter = Counter()
    coding_companies: set[str] = set()
    multi_round: Counter = Counter()

    for a in apps:
        meta = _parse_meta(a)
        ia = meta.get("interview_analytics") or {}
        if not isinstance(ia, dict):
            continue
        if ia.get("behavioral_result") in {"pass", "fail"}:
            behavioral_total += 1
            if ia.get("behavioral_result") == "pass":
                behavioral_pass += 1
        if ia.get("technical_result") in {"pass", "fail"}:
            technical_total += 1
            if ia.get("technical_result") == "pass":
                technical_pass += 1
        for q in ia.get("questions_asked") or []:
            if isinstance(q, str) and q.strip():
                questions[q.strip()] += 1
        for t in ia.get("weak_topics") or []:
            if isinstance(t, str) and t.strip():
                weak[t.strip()] += 1
        for t in ia.get("strong_topics") or []:
            if isinstance(t, str) and t.strip():
                strong[t.strip()] += 1
        if ia.get("asked_coding"):
            coding_companies.add(a.company)
        rounds = ia.get("interview_rounds")
        if isinstance(rounds, int) and rounds >= 2:
            multi_round[a.company] += 1
        elif normalize_status(a.status) in {"technical_interview", "hiring_manager", "final_interview"}:
            multi_round[a.company] += 1

    return {
        "behavioral_interview_pass_rate": _pct(behavioral_pass, behavioral_total),
        "technical_interview_pass_rate": _pct(technical_pass, technical_total),
        "behavioral_samples": behavioral_total,
        "technical_samples": technical_total,
        "questions_asked_most_often": [{"question": q, "count": n} for q, n in questions.most_common(10)],
        "weakest_interview_topics": [{"topic": t, "count": n} for t, n in weak.most_common(8)],
        "strongest_interview_topics": [{"topic": t, "count": n} for t, n in strong.most_common(8)],
        "companies_that_ask_coding_questions": sorted(coding_companies),
        "companies_with_multiple_interview_rounds": [
            {"company": c, "count": n} for c, n in multi_round.most_common(10)
        ],
        "note": "Interview topic/question stats appear only after you log them on an application’s analytics fields.",
    }


def build_charts(apps: list[Application]) -> dict[str, Any]:
    by_day: Counter = Counter()
    by_company: Counter = Counter()
    by_role: Counter = Counter()
    salaries: list[float] = []
    funnel = Counter()

    for a in apps:
        st = normalize_status(a.status)
        day = (a.date_applied or a.created_at.date()).isoformat()
        by_day[day] += 1
        by_company[a.company] += 1
        by_role[_role_bucket(a.position)] += 1
        sal = _salary_mid(a.salary)
        if sal:
            salaries.append(sal)
        funnel[st] += 1
        if a.date_applied or st in APPLIED_OR_LATER:
            funnel["__applied_bucket"] += 1

    days_sorted = sorted(by_day.items())
    funnel_order = [
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
    return {
        "applications_over_time": {"labels": [d for d, _ in days_sorted], "values": [n for _, n in days_sorted]},
        "applications_by_company": {
            "labels": [c for c, _ in by_company.most_common(12)],
            "values": [n for _, n in by_company.most_common(12)],
        },
        "applications_by_role": {
            "labels": [r for r, _ in by_role.most_common()],
            "values": [n for _, n in by_role.most_common()],
        },
        "salary_distribution": {
            "values": salaries,
            "buckets": _salary_buckets(salaries),
        },
        "interview_funnel": {
            "labels": [stage_label(s) for s in funnel_order if funnel.get(s)],
            "values": [funnel[s] for s in funnel_order if funnel.get(s)],
        },
        "response_rate_trend": _response_trend(apps),
    }


def _salary_buckets(salaries: list[float]) -> dict[str, Any]:
    edges = [0, 60000, 80000, 100000, 120000, 150000, 10**9]
    labels = ["<60k", "60–80k", "80–100k", "100–120k", "120–150k", "150k+"]
    counts = [0] * (len(edges) - 1)
    for s in salaries:
        for i in range(len(edges) - 1):
            if edges[i] <= s < edges[i + 1]:
                counts[i] += 1
                break
    return {"labels": labels, "values": counts}


def _response_trend(apps: list[Application]) -> dict[str, Any]:
    week_applied: Counter = Counter()
    week_reply: Counter = Counter()
    for a in apps:
        d = a.date_applied or a.created_at.date()
        week = d - timedelta(days=d.weekday())
        key = week.isoformat()
        st = normalize_status(a.status)
        if a.date_applied or st in APPLIED_OR_LATER:
            week_applied[key] += 1
        if st in {
            "recruiter_replied",
            "phone_screen",
            "technical_interview",
            "hiring_manager",
            "final_interview",
            "offer",
            "accepted",
        }:
            week_reply[key] += 1
    labels = sorted(set(week_applied) | set(week_reply))
    rates = []
    for lab in labels:
        rates.append(_pct(week_reply[lab], week_applied[lab]) if week_applied[lab] else None)
    return {"labels": labels, "values": rates}


def build_reports(apps: list[Application], db: Session) -> dict[str, Any]:
    kpis = build_kpis(apps, db)
    success = build_success_metrics(apps, db)
    charts = build_charts(apps)
    by_company = Counter(a.company for a in apps)
    by_role = Counter(_role_bucket(a.position) for a in apps)
    by_salary = Counter()
    by_score = Counter()
    for a in apps:
        sal = _salary_mid(a.salary)
        if sal is None:
            by_salary["Not listed"] += 1
        elif sal < 70000:
            by_salary["$60–70k"] += 1
        elif sal < 90000:
            by_salary["$70–90k"] += 1
        elif sal < 120000:
            by_salary["$90–120k"] += 1
        else:
            by_salary["$120k+"] += 1
        score = float(a.application_score or 0)
        bucket = f"{int(score // 10) * 10}-{int(score // 10) * 10 + 9}"
        by_score[bucket] += 1

    return {
        "weekly_job_search_report": {
            "period": "last_7_days",
            "applications": kpis["applications_this_week"],
            "replies": kpis["recruiter_replies"],
            "interviews": kpis["interview_invitations"],
            "offers": kpis["job_offers"],
            "insights": build_insights(apps, kpis, success)[:5],
        },
        "monthly_performance_report": {
            "period": "month_to_date",
            "applications": kpis["applications_this_month"],
            "response_rate": kpis["recruiter_response_rate"],
            "interview_rate": kpis["interview_rate"],
            "offer_rate": kpis["offer_rate"],
            "rejections": kpis["rejections"],
            "ghosted": kpis["ghosted_applications"],
        },
        "applications_by_company": dict(by_company.most_common()),
        "applications_by_role": dict(by_role.most_common()),
        "applications_by_salary": dict(by_salary),
        "applications_by_match_score": dict(sorted(by_score.items())),
        "interview_conversion_funnel": charts["interview_funnel"],
        "response_rate_trend": charts["response_rate_trend"],
    }


def build_analytics_dashboard(db: Session) -> dict[str, Any]:
    apps = load_applications(db)
    kpis = build_kpis(apps, db)
    success = build_success_metrics(apps, db)
    insights = build_insights(apps, kpis, success)
    followups = build_followups(apps)
    interview = build_interview_analytics(apps)
    charts = build_charts(apps)
    reports = build_reports(apps, db)
    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "mode": "recruiter_analytics",
        "fabricated": False,
        "sample_size": len(apps),
        "kpis": kpis,
        "success_metrics": success,
        "insights": insights,
        "followups": followups,
        "interview_analytics": interview,
        "charts": charts,
        "reports": reports,
        "stages": [
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
        ],
        "auto_send_followups": False,
        "note": "Statistics are derived only from applications stored in the local Job Machine database.",
    }


def applications_as_rows(apps: list[Application]) -> list[dict[str, Any]]:
    rows = []
    for a in apps:
        meta = _parse_meta(a)
        rows.append(
            {
                "id": a.id,
                "company": a.company,
                "position": a.position,
                "salary": a.salary,
                "location": a.location,
                "status": normalize_status(a.status),
                "stage_label": stage_label(a.status),
                "date_applied": a.date_applied.isoformat() if a.date_applied else "",
                "follow_up_date": a.follow_up_date.isoformat() if a.follow_up_date else "",
                "interview_date": a.interview_date.isoformat() if a.interview_date else "",
                "recruiter_name": a.recruiter_name,
                "recruiter_email": a.recruiter_email,
                "application_score": a.application_score,
                "resume_version": meta.get("resume_version", "default"),
                "cover_version": meta.get("cover_version", "default"),
                "notes": a.notes,
            }
        )
    return rows


def export_csv(apps: list[Application]) -> str:
    rows = applications_as_rows(apps)
    if not rows:
        return "id,company,position,status\n"
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def export_json(db: Session) -> str:
    return json.dumps(build_analytics_dashboard(db), indent=2)


def export_excel_bytes(apps: list[Application]) -> bytes:
    try:
        from openpyxl import Workbook
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("openpyxl is required for Excel export") from exc
    wb = Workbook()
    ws = wb.active
    ws.title = "Applications"
    rows = applications_as_rows(apps)
    if not rows:
        ws.append(["id", "company", "position", "status"])
    else:
        headers = list(rows[0].keys())
        ws.append(headers)
        for r in rows:
            ws.append([r.get(h, "") for h in headers])
    bio = io.BytesIO()
    wb.save(bio)
    return bio.getvalue()


def export_pdf_bytes(db: Session) -> bytes:
    """Simple text PDF report from real KPIs only."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("reportlab is required for PDF export") from exc

    data = build_analytics_dashboard(db)
    bio = io.BytesIO()
    c = canvas.Canvas(bio, pagesize=letter)
    width, height = letter
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Leroy Garvin Jr — Recruiter Analytics Report")
    y -= 20
    c.setFont("Helvetica", 9)
    c.drawString(50, y, f"Generated: {data['generated_at']}  |  Sample size: {data['sample_size']}  |  No fabricated stats")
    y -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "KPIs")
    y -= 16
    c.setFont("Helvetica", 9)
    for k, v in data["kpis"].items():
        if k == "data_note":
            continue
        c.drawString(60, y, f"{k.replace('_', ' ').title()}: {v}")
        y -= 12
        if y < 60:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 9)
    y -= 10
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Insights (from tracked data only)")
    y -= 16
    c.setFont("Helvetica", 9)
    for line in data["insights"]:
        for chunk in _wrap(line, 95):
            c.drawString(60, y, chunk)
            y -= 12
            if y < 60:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 9)
    c.showPage()
    c.save()
    return bio.getvalue()


def _wrap(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        trial = " ".join(cur + [w])
        if len(trial) > width:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(" ".join(cur))
    return lines or [""]
