# n8n Workflow Inventory

**Source of truth:** Workflow definition JSON exports in `Desktop/GH-X/workflows`  
**Also reviewed:** Local `~/.n8n` database (stub only)  
**Execution evidence:** Empty / not found — do not claim production results  
**Date:** 2026-07-20

## Status legend
- **Prototype** — incomplete or stub definition
- **Functional Build** — connected definition with integrations; not proven executed
- **In Progress** — partial / unclear (use only when justified)
- **Production Ready** — requires execution + privacy-safe evidence (none currently)

## Inventory

| Workflow | Group | Purpose (definition) | Trigger | Main nodes (count) | Integrations | AI Used | Execution Evidence | Current Status | Sensitive Data Risk | Portfolio Score | Include |
|----------|-------|----------------------|---------|--------------------|--------------|---------|--------------------|----------------|---------------------|-----------------|---------|
| Design + Reel Prompt Generator | B | On a schedule, search records, build design/reel prompts in Code nodes, and upda… | Schedule Trigger | 6 | Airtable, Code, Schedule Trigger, Split In Batches | No/Needs Review | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GH-X OpenAI Image Generator | C | On a schedule, find design-ready rows, call OpenAI Images via HTTP, store via Go… | Schedule · Cover Image Run | 10 | Airtable, Code, Google Drive, HTTP Request, IF | Yes | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-00-Error-Alerts | H | Catch n8n workflow errors and route them through filtering/alerting logic.… | Error Trigger | 5 | Code, Error Trigger, HTTP Request, IF, NoOp | No/Needs Review | None found | Functional Build | Medium | Needs Review (score after capture) | Yes |
| GHX-01-Idea-Intelligence | A | On a schedule, generate product ideas (OpenAI HTTP) and create Airtable product … | Schedule · Weekly Ideas | 5 | Airtable, Code, HTTP Request, OpenAI (via HTTP), Schedule Trigger | Yes | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-03-Etsy-Metricool-Handoff | D | On a schedule, search ready rows and prepare/save draft handoff fields in Airtab… | Schedule · Publishing Prep | 4 | Airtable, Code, Schedule Trigger | No/Needs Review | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-03B-Product-File-Uploader | C | On a schedule, build product blueprints/images via OpenAI HTTP and write product… | Schedule · Product File Run | 22 | Airtable, Code, Google Drive, HTTP Request, IF | Yes | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-04-Mockup-Generator | C | On a schedule, process mockup queue rows with OpenAI Chat + Images, store assets… | Schedule · Mockup Run | 15 | Airtable, Code, Google Drive, HTTP Request, IF | Yes | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-05-Social-Asset-Generator | C | On a schedule, process social queue rows with OpenAI Chat via HTTP and update Ai… | Schedule · Social Run | 10 | Airtable, Code, HTTP Request, IF, OpenAI (via HTTP) | Yes | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-06-Publish-Queue-Manager | D | On a schedule, validate ready-to-publish rows and mark publish-ready or append e… | Schedule · Validation Run | 8 | Airtable, Code, IF, Schedule Trigger, Split In Batches | No/Needs Review | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-07-Etsy-Draft-Publisher | D | On a schedule, create Etsy draft listings and upload images/digital files via HT… | Schedule · Etsy Draft Run | 18 | Airtable, Code, Etsy (via HTTP), HTTP Request, IF | No/Needs Review | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-07-Performance-Tracker | G | On a schedule, review published rows, generate notes via OpenAI HTTP, and save m… | Schedule · Weekly Performance | 8 | Airtable, Code, HTTP Request, OpenAI (via HTTP), Schedule Trigger | Yes | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-08-Metricool-Scheduler | E | On a schedule, build social posts (OpenAI + Metricool HTTP) and mark scheduled /… | Schedule · Social Schedule Run | 16 | Airtable, Code, HTTP Request, IF, Metricool (via HTTP) | Yes | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-09-Ready-To-Post-Queue | E | On a schedule, find scheduled content and create ready-to-post queue rows in Air… | Schedule · Every Hour | 11 | Airtable, Code, IF, Schedule Trigger, Split In Batches | No/Needs Review | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-09-Self-Healing-QA | H | On a schedule, find failed rows and requeue for retry or flag for manual review … | Schedule · QA Sweep | 11 | Airtable, Code, HTTP Request, IF, NoOp | No/Needs Review | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-10-Performance-Tracker | G | On a schedule, fetch live product metrics (Etsy HTTP + OpenAI notes) and save me… | Schedule · Weekly Metrics | 12 | Airtable, Code, Etsy (via HTTP), HTTP Request, IF | Yes | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-11-Winning-Idea-Loop | A | On a schedule, read top-performing rows, generate new ideas via OpenAI HTTP, and… | Schedule · Weekly Idea Loop | 9 | Airtable, Code, HTTP Request, IF, NoOp | Yes | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-12-Content-Idea-Generator | A | On a schedule, find promotable products, generate content ideas via OpenAI HTTP,… | Schedule · Daily Content Ideas | 12 | Airtable, Code, HTTP Request, IF, OpenAI (via HTTP) | Yes | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-13-Video-Script-Builder | F | On a schedule, generate video scripts via OpenAI HTTP for queued rows and save s… | Schedule · Script Build Run | 10 | Airtable, Code, HTTP Request, IF, OpenAI (via HTTP) | Yes | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-14-Metricool-Content-Scheduler | E | On a schedule, process content queue rows, schedule via Metricool HTTP, and save… | Schedule · Metricool Content Run | 16 | Airtable, Code, HTTP Request, IF, Metricool (via HTTP) | Yes | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-15-Content-QA | F | On a schedule, review QA queue rows and mark video-ready or needs-fix in Airtabl… | Schedule · Content QA Sweep | 8 | Airtable, Code, IF, Schedule Trigger, Split In Batches | No/Needs Review | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-16-HeyGen-Video-Generator | F | On a schedule, create HeyGen videos for video-ready rows and mark processing or … | Schedule · Every 15 Minutes | 13 | Airtable, Code, HTTP Request, HeyGen (via HTTP), IF | Yes | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-17-HeyGen-Status-Poller | F | On a schedule, poll HeyGen status for processing videos and update Airtable read… | Schedule · Every 10 Minutes | 14 | Airtable, Code, HTTP Request, HeyGen (via HTTP), IF | Yes | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |
| GHX-Generate-Product-Listing | B | On a schedule, search idea records, generate listing JSON via OpenAI HTTP, and u… | Schedule · Listing Run | 10 | Airtable, Code, HTTP Request, IF, OpenAI (via HTTP) | Yes | None found | Functional Build | High until sanitized export/screenshots | Needs Review (score after capture) | Yes |

## Local stub (separate)
| Workflow | Status | Notes |
|----------|--------|-------|
| GH-X Master Automation | Prototype | Manual Trigger → Airtable Search; empty base/table; 0 executions |

## Duplicates / collisions (Needs Review)
- Two workflows use **GHX-07** prefix: Etsy Draft Publisher vs Performance Tracker
- Two workflows use **GHX-09** prefix: Ready-To-Post Queue vs Self-Healing QA
- Backup file `GHX-03B-Product-File-Uploader.backup-pre-v3.json` excluded from portfolio projects
