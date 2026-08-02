# AI Career Agent — Production Report

**Date:** 2026-08-02  
**Commit target:** Job Machine additive modules only  
**Auto-apply:** OFF · **Auto-email:** OFF · **Approval required:** YES  

## New modules

| Module | Path | Purpose |
|--------|------|---------|
| Career Agent | `app/services/career_agent.py` | 8:00 AM run via existing `morning_refresh` + Daily Brief + ≥80% notifications |
| Career Coach | `app/services/career_coach.py` | Resume/portfolio/ATS/interview/salary gap analysis + weekly report |
| Recruiter CRM | `app/services/recruiter_crm.py` + `RecruiterContact` model | Local recruiter tracking; never emails |
| Interview Intelligence | `app/services/interview_intelligence.py` | Pre-interview brief from posting + verified portfolio/profile |
| API router | `app/routers/career_agent_api.py` | `/api/career-agent/*` (additive; existing routes untouched) |
| UI | `static/index.html` + `static/js/app.js` | New **AI Career Agent** tab |

## Morning agent behavior (8:00 AM local)

1. Search supported remote boards (`morning_refresh` → existing `search_jobs`)  
2. Remove expired / unverified remote listings (existing purge)  
3. Surface new jobs (`found_at` today)  
4. Score with transparent Match Score engine (existing `score_job`)  
5. Build tailored packets (`prepare_top_packets`)  
6. **Never auto-submit**  
7. Notify in Daily Brief only when Match Score **≥ 80%**

## Daily Brief fields

- New jobs found  
- Best opportunities  
- Highest interview probability (= highest Match Score; not invented %)  
- Companies hiring repeatedly  
- Salary trends (listed salaries only)  
- Missing skills appearing frequently  
- Recommended certifications (**research only; held_by_leroy=false**)  
- Recruiters viewing applications (`recruiter_viewed`)  
- Follow-ups due today  
- Upcoming interviews  
- Jobs closing within 48 hours (**only when deadline is stored/parseable**)  

## Safety / truth

- No invented experience, education, or certifications  
- Interview Intelligence leaves financials/competitors/news **unavailable** unless present in posting text  
- CRM / follow-ups never send email  
- Existing Job Finder, Approve-to-Apply, Analytics, Assistant, Autofill routes unchanged  

## API surface (new)

- `GET /api/career-agent/status`  
- `POST /api/career-agent/run-morning`  
- `GET /api/career-agent/daily-brief`  
- `GET /api/career-agent/coach`  
- `GET|POST /api/career-agent/coach/weekly-report`  
- `GET|POST|PATCH|DELETE /api/career-agent/crm...`  
- `GET|POST /api/career-agent/interview-intelligence`  

## Tests

`tests/test_career_agent.py` — Daily Brief notifications, coach truth rules, CRM no auto-email, Interview Intelligence no fabricated finance.

Run: `pytest -q`

## Scheduler note

`app/main.py` `_morning_loop` now calls `run_career_agent_morning` (which **calls** unchanged `morning_refresh`).  
`POST /api/pipeline/morning-refresh` remains available and unchanged.
