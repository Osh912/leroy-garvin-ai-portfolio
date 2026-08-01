# Technical Documentation — GHX-15-Content-QA

## Overview
QA-gate content/video readiness in Airtable (ready vs needs fix).

| Field | Value |
|-------|-------|
| Export file | `GHX-15-Content-QA.json` |
| Active in export | `False` |
| Nodes / connections | 8 / 9 |
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
| Schedule · Content QA Sweep | scheduleTrigger | Schedule |
| Airtable · Search QA Queue | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Validate Content Fields | code | Code |
| Filter · Content Complete | if | — |
| Airtable · Mark Video Ready | airtable | update |
| Airtable · Mark Needs Fix | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Content QA Sweep` → `Airtable · Search QA Queue`
- `Airtable · Search QA Queue` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Validate Content Fields`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Validate Content Fields` → `Filter · Content Complete`
- `Filter · Content Complete` → `Airtable · Mark Video Ready`
- `Filter · Content Complete` → `Airtable · Mark Needs Fix`
- `Airtable · Mark Video Ready` → `Batch · Split Records`
- `Airtable · Mark Needs Fix` → `Batch · Split Records`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
