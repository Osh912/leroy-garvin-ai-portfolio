# Technical Documentation — GHX-Generate-Product-Listing

## Overview
Turn idea rows into product listing JSON via OpenAI and update Airtable success/error fields.

| Field | Value |
|-------|-------|
| Export file | `GHX-Generate-Product-Listing.json` |
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
| Schedule · Listing Run | scheduleTrigger | Schedule |
| Airtable · Search Ideas | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Build Chat Payload | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP |
| Code · Parse Listing JSON | code | Code |
| Filter · Parse OK | if | — |
| Airtable · Update Success | airtable | update |
| Airtable · Update Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Listing Run` → `Airtable · Search Ideas`
- `Airtable · Search Ideas` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build Chat Payload`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Build Chat Payload` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Parse Listing JSON`
- `Code · Parse Listing JSON` → `Filter · Parse OK`
- `Filter · Parse OK` → `Airtable · Update Success`
- `Filter · Parse OK` → `Airtable · Update Error`
- `Airtable · Update Success` → `Batch · Split Records`
- `Airtable · Update Error` → `Batch · Split Records`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
