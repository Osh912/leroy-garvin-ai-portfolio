# Technical Documentation — GHX-07-Performance-Tracker

## Overview
Write performance notes for published rows via OpenAI and save metrics fields in Airtable.

| Field | Value |
|-------|-------|
| Export file | `GHX-07-Performance-Tracker.json` |
| Active in export | `False` |
| Nodes / connections | 8 / 8 |
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
| Schedule · Weekly Performance | scheduleTrigger | Schedule |
| Airtable · Search Published | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Score Metrics | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP |
| Code · Merge AI Notes | code | Code |
| Airtable · Save Metrics | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Weekly Performance` → `Airtable · Search Published`
- `Airtable · Search Published` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Score Metrics`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Score Metrics` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Merge AI Notes`
- `Code · Merge AI Notes` → `Airtable · Save Metrics`
- `Airtable · Save Metrics` → `Batch · Split Records`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
