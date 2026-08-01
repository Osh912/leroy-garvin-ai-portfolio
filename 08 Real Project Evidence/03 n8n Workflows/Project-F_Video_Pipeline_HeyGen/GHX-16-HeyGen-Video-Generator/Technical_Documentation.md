# Technical Documentation — GHX-16-HeyGen-Video-Generator

## Overview
Request HeyGen video creation for video-ready rows and mark processing/errors in Airtable.

| Field | Value |
|-------|-------|
| Export file | `GHX-16-HeyGen-Video-Generator.json` |
| Active in export | `False` |
| Nodes / connections | 13 / 15 |
| Complexity | Intermediate |
| Status | Functional Build (not Production Ready) |

## Services & integrations
- Airtable
- HTTP Request
- HeyGen API
- n8n Code
- n8n Schedule Trigger

## AI / APIs
- HTTP · HeyGen Create Video → HeyGen API


**Needs Review:** Exact model IDs and secrets are not published.

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Every 15 Minutes | scheduleTrigger | Schedule |
| Set · Load HeyGen Config | set | — |
| Code · Setup Config | code | Code |
| Airtable · Search Video Ready | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Build HeyGen Payload | code | Code |
| Filter · Payload OK | if | — |
| HTTP · HeyGen Create Video | httpRequest | HTTP |
| Code · Parse HeyGen Response | code | Code |
| Filter · Video Id Returned | if | — |
| Airtable · Mark Video Processing | airtable | update |
| Airtable · Log HeyGen Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Every 15 Minutes` → `Set · Load HeyGen Config`
- `Set · Load HeyGen Config` → `Code · Setup Config`
- `Code · Setup Config` → `Airtable · Search Video Ready`
- `Airtable · Search Video Ready` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build HeyGen Payload`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Build HeyGen Payload` → `Filter · Payload OK`
- `Filter · Payload OK` → `HTTP · HeyGen Create Video`
- `Filter · Payload OK` → `Airtable · Log HeyGen Error`
- `HTTP · HeyGen Create Video` → `Code · Parse HeyGen Response`
- `Code · Parse HeyGen Response` → `Filter · Video Id Returned`
- `Filter · Video Id Returned` → `Airtable · Mark Video Processing`
- `Filter · Video Id Returned` → `Airtable · Log HeyGen Error`
- `Airtable · Mark Video Processing` → `Batch · Split Records`
- `Airtable · Log HeyGen Error` → `Batch · Split Records`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
