# Technical Documentation — GHX-09-Ready-To-Post-Queue

## Overview
Create ready-to-post queue rows from scheduled content records in Airtable.

| Field | Value |
|-------|-------|
| Export file | `GHX-09-Ready-To-Post-Queue.json` |
| Active in export | `False` |
| Nodes / connections | 11 / 12 |
| Complexity | Intermediate |
| Status | Functional Build (not Production Ready) |

## Services & integrations
- Airtable
- n8n Code
- n8n Schedule Trigger

## AI / APIs
- None detected in definition


**Needs Review:** Exact model IDs and secrets are not published.

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Every Hour | scheduleTrigger | Schedule |
| Code · Reset Run Counters | code | Code |
| Airtable · Search Scheduled Content | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Build Ready-To-Post Queue Items | code | Code |
| Filter · Queue Item OK | if | — |
| Airtable · Create Ready To Post Row | airtable | create |
| Airtable · Mark Queued To Post | airtable | update |
| Code · Log Queued Item | code | Code |
| Code · Log Skipped Item | code | Code |
| Code · Run Summary | code | Code |

## Connections
- `Schedule · Every Hour` → `Code · Reset Run Counters`
- `Code · Reset Run Counters` → `Airtable · Search Scheduled Content`
- `Airtable · Search Scheduled Content` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build Ready-To-Post Queue Items`
- `Batch · Split Records` → `Code · Run Summary`
- `Code · Build Ready-To-Post Queue Items` → `Filter · Queue Item OK`
- `Filter · Queue Item OK` → `Airtable · Create Ready To Post Row`
- `Filter · Queue Item OK` → `Code · Log Skipped Item`
- `Airtable · Create Ready To Post Row` → `Airtable · Mark Queued To Post`
- `Airtable · Mark Queued To Post` → `Code · Log Queued Item`
- `Code · Log Queued Item` → `Batch · Split Records`
- `Code · Log Skipped Item` → `Batch · Split Records`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
