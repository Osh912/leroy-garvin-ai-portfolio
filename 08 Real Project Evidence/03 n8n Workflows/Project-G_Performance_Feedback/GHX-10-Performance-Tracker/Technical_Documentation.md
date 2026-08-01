# Technical Documentation — GHX-10-Performance-Tracker

## Overview
Fetch live listing context (Etsy HTTP) plus OpenAI notes and save metrics in Airtable.

| Field | Value |
|-------|-------|
| Export file | `GHX-10-Performance-Tracker.json` |
| Active in export | `False` |
| Nodes / connections | 12 / 13 |
| Complexity | Advanced |
| Status | Functional Build (not Production Ready) |

## Services & integrations
- Airtable
- Etsy API
- HTTP Request
- OpenAI API
- n8n Code
- n8n Schedule Trigger

## AI / APIs
- HTTP · OpenAI Notes → OpenAI Chat Completions API
- OpenAI Chat Completions API

**Needs Review:** Exact model IDs and secrets are not published.

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Weekly Metrics | scheduleTrigger | Schedule |
| Airtable · Search Live Products | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Prep Metrics Context | code | Code |
| Filter · Has Etsy Listing | if | — |
| HTTP · Etsy Get Listing | httpRequest | HTTP |
| Code · Score Metrics | code | Code |
| Code · Score Without Etsy | code | Code |
| HTTP · OpenAI Notes | httpRequest | HTTP |
| Code · Merge AI Notes | code | Code |
| Airtable · Save Metrics | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Weekly Metrics` → `Airtable · Search Live Products`
- `Airtable · Search Live Products` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Prep Metrics Context`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Prep Metrics Context` → `Filter · Has Etsy Listing`
- `Filter · Has Etsy Listing` → `HTTP · Etsy Get Listing`
- `Filter · Has Etsy Listing` → `Code · Score Without Etsy`
- `HTTP · Etsy Get Listing` → `Code · Score Metrics`
- `Code · Score Metrics` → `HTTP · OpenAI Notes`
- `Code · Score Without Etsy` → `HTTP · OpenAI Notes`
- `HTTP · OpenAI Notes` → `Code · Merge AI Notes`
- `Code · Merge AI Notes` → `Airtable · Save Metrics`
- `Airtable · Save Metrics` → `Batch · Split Records`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
