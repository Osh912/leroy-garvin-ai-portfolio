# Technical Documentation — GHX-14-Metricool-Content-Scheduler

## Overview
Schedule content-queue posts via Metricool HTTP and save post packs or errors in Airtable.

| Field | Value |
|-------|-------|
| Export file | `GHX-14-Metricool-Content-Scheduler.json` |
| Active in export | `False` |
| Nodes / connections | 16 / 19 |
| Complexity | Advanced |
| Status | Functional Build (not Production Ready) |

## Services & integrations
- Airtable
- HTTP Request
- Metricool API
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
| Schedule · Metricool Content Run | scheduleTrigger | Schedule |
| Set · Load Metricool Config | set | — |
| Code · Setup Config | code | Code |
| Airtable · Search Content Queue | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Build Metricool Pack Body | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP |
| Code · Expand Metricool Posts | code | Code |
| Filter · Pack OK | if | — |
| Filter · API Enabled | if | — |
| HTTP · Metricool Schedule Post | httpRequest | HTTP |
| Code · Aggregate Metricool Results | code | Code |
| Filter · Schedule OK | if | — |
| Airtable · Save Post Pack | airtable | update |
| Airtable · Log Scheduler Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Metricool Content Run` → `Set · Load Metricool Config`
- `Set · Load Metricool Config` → `Code · Setup Config`
- `Code · Setup Config` → `Airtable · Search Content Queue`
- `Airtable · Search Content Queue` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build Metricool Pack Body`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Build Metricool Pack Body` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Expand Metricool Posts`
- `Code · Expand Metricool Posts` → `Filter · Pack OK`
- `Filter · Pack OK` → `Filter · API Enabled`
- `Filter · Pack OK` → `Airtable · Log Scheduler Error`
- `Filter · API Enabled` → `HTTP · Metricool Schedule Post`
- `Filter · API Enabled` → `Airtable · Save Post Pack`
- `HTTP · Metricool Schedule Post` → `Code · Aggregate Metricool Results`
- `Code · Aggregate Metricool Results` → `Filter · Schedule OK`
- `Filter · Schedule OK` → `Airtable · Save Post Pack`
- `Filter · Schedule OK` → `Airtable · Log Scheduler Error`
- `Airtable · Save Post Pack` → `Batch · Split Records`
- `Airtable · Log Scheduler Error` → `Batch · Split Records`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
