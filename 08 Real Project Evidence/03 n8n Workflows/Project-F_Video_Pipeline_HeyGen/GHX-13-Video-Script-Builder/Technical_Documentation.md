# Technical Documentation — GHX-13-Video-Script-Builder

## Overview
Generate video scripts via OpenAI Chat for queued rows and save scripts/errors in Airtable.

| Field | Value |
|-------|-------|
| Export file | `GHX-13-Video-Script-Builder.json` |
| Active in export | `False` |
| Nodes / connections | 10 / 11 |
| Complexity | Intermediate |
| Status | Functional Build (not Production Ready) |

## Services & integrations
- Airtable
- HTTP Request
- OpenAI API
- n8n Code
- n8n Schedule Trigger

## AI / APIs
- HTTP · OpenAI Chat → OpenAI Chat Completions API
- OpenAI Chat Completions API

**Needs Review:** Exact model IDs and secrets are not published.

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Script Build Run | scheduleTrigger | Schedule |
| Airtable · Search Script Queue | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Build Script Body | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP |
| Code · Parse Platform Scripts | code | Code |
| Filter · Script OK | if | — |
| Airtable · Save Scripts | airtable | update |
| Airtable · Log Script Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Script Build Run` → `Airtable · Search Script Queue`
- `Airtable · Search Script Queue` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build Script Body`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Build Script Body` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Parse Platform Scripts`
- `Code · Parse Platform Scripts` → `Filter · Script OK`
- `Filter · Script OK` → `Airtable · Save Scripts`
- `Filter · Script OK` → `Airtable · Log Script Error`
- `Airtable · Save Scripts` → `Batch · Split Records`
- `Airtable · Log Script Error` → `Batch · Split Records`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
