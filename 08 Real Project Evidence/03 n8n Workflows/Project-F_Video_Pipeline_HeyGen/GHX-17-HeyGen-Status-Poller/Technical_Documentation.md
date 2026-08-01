# Technical Documentation — GHX-17-HeyGen-Status-Poller

## Overview
Poll HeyGen job status and update Airtable ready/failed/error fields.

| Field | Value |
|-------|-------|
| Export file | `GHX-17-HeyGen-Status-Poller.json` |
| Active in export | `False` |
| Nodes / connections | 14 / 18 |
| Complexity | Intermediate |
| Status | Functional Build (not Production Ready) |

## Services & integrations
- Airtable
- HTTP Request
- HeyGen API
- n8n Code
- n8n Schedule Trigger

## AI / APIs
- HTTP · HeyGen Get Status → HeyGen API


**Needs Review:** Exact model IDs and secrets are not published.

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Every 10 Minutes | scheduleTrigger | Schedule |
| Airtable · Search Processing Videos | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Prepare Poll Context | code | Code |
| Filter · Context OK | if | — |
| HTTP · HeyGen Get Status | httpRequest | HTTP |
| Code · Parse HeyGen Status | code | Code |
| Switch · HeyGen Status | switch | — |
| Airtable · Mark Ready To Schedule | airtable | update |
| Code · Log Still Processing | code | Code |
| Airtable · Mark Video Failed | airtable | update |
| Airtable · Log Poll Error | airtable | update |
| Airtable · Log Context Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Every 10 Minutes` → `Airtable · Search Processing Videos`
- `Airtable · Search Processing Videos` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Prepare Poll Context`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Prepare Poll Context` → `Filter · Context OK`
- `Filter · Context OK` → `HTTP · HeyGen Get Status`
- `Filter · Context OK` → `Airtable · Log Context Error`
- `HTTP · HeyGen Get Status` → `Code · Parse HeyGen Status`
- `Code · Parse HeyGen Status` → `Switch · HeyGen Status`
- `Switch · HeyGen Status` → `Airtable · Mark Ready To Schedule`
- `Switch · HeyGen Status` → `Code · Log Still Processing`
- `Switch · HeyGen Status` → `Airtable · Mark Video Failed`
- `Switch · HeyGen Status` → `Airtable · Log Poll Error`
- `Airtable · Mark Ready To Schedule` → `Batch · Split Records`
- `Code · Log Still Processing` → `Batch · Split Records`
- `Airtable · Mark Video Failed` → `Batch · Split Records`
- `Airtable · Log Poll Error` → `Batch · Split Records`
- `Airtable · Log Context Error` → `Batch · Split Records`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
