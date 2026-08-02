# Autonomous Career Agent 2.0 — Report

## Confirmation

**RUN NOW** is available at any time via the **AI Career Agent** tab (`#btn-career-run-now` → `POST /api/career-agent/run-now`).  
You do **not** need to wait for the 8:00 AM scheduler.

Safety unchanged: **never auto-submit · never auto-email · approval-only · no invented interview probabilities**.

## Files changed (high level)

- `app/config.py` — expanded Greenhouse/Lever/Ashby + Workable employers  
- `app/services/sources/__init__.py` — Workable fetcher + retry helper  
- `app/services/job_finder.py` — concurrent `asyncio.gather` source search + logging  
- `app/services/filters.py` — target roles, contract/spam/stale rejects, US `(US)` location  
- `app/services/scorer.py` — Match Score **v2** weights (explainable)  
- `app/services/career_agent.py` — RUN NOW, Today's Brief, 90%+ alerts, locks  
- `app/services/agent_log.py`, `company_cache.py` — action log + company cache  
- `app/services/recruiter_crm.py` + `models.py` + `database.py` — CRM fields  
- `app/routers/career_agent_api.py` — `/run-now`, `/todays-brief`  
- `static/index.html`, `static/js/app.js` — RUN NOW + Today's Brief UI  
- Tests: `tests/test_agent_2.py`, `tests/test_core.py` scoring assertions  

Existing APIs (`/api/jobs/*`, `/api/applications/*`, `/api/analytics/*`, `/api/assistant/*`, `/api/autofill/*`, `/api/pipeline/*`) remain.

## New modules

| Module | Role |
|--------|------|
| `agent_log.py` | Action logging + duplicate-run lock |
| `company_cache.py` | 12h local company packet cache |
| Match Score v2 | Skill 35% · Interview readiness 25% · Remote 15% · Salary 10% · Growth 5% · Resume 5% · Portfolio 5% |
| Today's Brief | Dashboard stats for today’s search + funnel |
| `POST /run-now` | Manual full agent run |

## Tests passed

**42 pytest passed** · Compatibility smoke: dashboard, analytics, assistant, autofill, career-agent, pipeline stages.

## Performance improvements

- Concurrent board/ATS fetches (`asyncio.gather`)  
- One retry on failed/rate-limited sources  
- Duplicate-run lock (prevents overlapping searches; RUN NOW can force)  
- Company cache for top packet metadata  
- Action log under `data/agent_actions.log`  

## New capabilities

- Expanded ATS/employer coverage (Workable + more Greenhouse/Lever/Ashby boards)  
- Stricter rejects: contract-only, commission-only, spam, listings >30 days (unless reposted)  
- Broader target-role keywords  
- Explainable Match Score v2 (`interview_probability` still **null**)  
- Notifications: 90%+ matches, 80%+ matches, replies, interviews, follow-ups, high-pay, 48h closings  
- Today's Brief dashboard  
- CRM: role, application date, status, referral source  

## Example daily workflow

1. Open Job Machine → **AI Career Agent**  
2. Click **RUN NOW** (or wait for 8:00 AM)  
3. Review **Today's Brief** + notifications (≥90% alerts)  
4. Open Top 10 → Application Assistant → Prepare / Open Application  
5. Approve to Apply only when ready · Mark Submitted after you submit  
6. Log CRM + Interview Intelligence before screens  
7. Weekly Report from Career Coach  

## Async correctness

- Morning loop / RUN NOW `await run_career_agent_morning` / `await run_now`  
- `search_jobs` uses `await asyncio.gather` for all sources  
- `fetch_with_retry` awaits each attempt  
- Active URL checks remain awaited via existing `verify_jobs_active`  
