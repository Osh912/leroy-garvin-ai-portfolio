# Technical Documentation — GHX-05-Social-Asset-Generator

## Overview
Generate social asset copy/content via OpenAI Chat and update Airtable social queue rows.

| Field | Value |
|-------|-------|
| Export file | `GHX-05-Social-Asset-Generator.json` |
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
| Schedule · Social Run | scheduleTrigger | Schedule |
| Airtable · Search Social Queue | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Build Social Chat Body | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP |
| Code · Parse Social JSON | code | Code |
| Filter · Parse OK | if | — |
| Airtable · Update Success | airtable | update |
| Airtable · Update Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Social Run` → `Airtable · Search Social Queue`
- `Airtable · Search Social Queue` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build Social Chat Body`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Build Social Chat Body` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Parse Social JSON`
- `Code · Parse Social JSON` → `Filter · Parse OK`
- `Filter · Parse OK` → `Airtable · Update Success`
- `Filter · Parse OK` → `Airtable · Update Error`
- `Airtable · Update Success` → `Batch · Split Records`
- `Airtable · Update Error` → `Batch · Split Records`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
