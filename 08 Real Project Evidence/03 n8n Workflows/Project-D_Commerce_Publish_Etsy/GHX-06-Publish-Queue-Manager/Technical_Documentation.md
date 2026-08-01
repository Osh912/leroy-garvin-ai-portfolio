# Technical Documentation — GHX-06-Publish-Queue-Manager

## Overview
Validate ready-to-publish rows and mark publish-ready or log errors in Airtable.

| Field | Value |
|-------|-------|
| Export file | `GHX-06-Publish-Queue-Manager.json` |
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
| Schedule · Validation Run | scheduleTrigger | Schedule |
| Airtable · Search Ready To Publish | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Validate Publish Gate | code | Code |
| Filter · Complete | if | — |
| Airtable · Mark Publish Ready | airtable | update |
| Airtable · Append Error Log | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Validation Run` → `Airtable · Search Ready To Publish`
- `Airtable · Search Ready To Publish` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Validate Publish Gate`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Validate Publish Gate` → `Filter · Complete`
- `Filter · Complete` → `Airtable · Mark Publish Ready`
- `Filter · Complete` → `Airtable · Append Error Log`
- `Airtable · Mark Publish Ready` → `Batch · Split Records`
- `Airtable · Append Error Log` → `Batch · Split Records`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
