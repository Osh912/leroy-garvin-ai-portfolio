# Technical Documentation — GHX-08-Metricool-Scheduler

## Overview
Build and schedule social posts via OpenAI + Metricool HTTP; update Airtable schedule status.

| Field | Value |
|-------|-------|
| Export file | `GHX-08-Metricool-Scheduler.json` |
| Active in export | `False` |
| Nodes / connections | 16 / 18 |
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
| Schedule · Social Schedule Run | scheduleTrigger | Schedule |
| Set · Load Metricool Config | set | — |
| Code · Setup Config | code | Code |
| Airtable · Search Social Queue | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Build Caption Body | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP |
| Code · Expand Platform Posts | code | Code |
| Filter · API Enabled | if | — |
| HTTP · Metricool Schedule Post | httpRequest | HTTP |
| Code · Aggregate Schedule Results | code | Code |
| Filter · Schedule OK | if | — |
| Airtable · Mark Scheduled | airtable | update |
| Airtable · Log Schedule Error | airtable | update |
| Airtable · Save Dry Run Post Pack | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Social Schedule Run` → `Set · Load Metricool Config`
- `Set · Load Metricool Config` → `Code · Setup Config`
- `Code · Setup Config` → `Airtable · Search Social Queue`
- `Airtable · Search Social Queue` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build Caption Body`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Build Caption Body` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Expand Platform Posts`
- `Code · Expand Platform Posts` → `Filter · API Enabled`
- `Filter · API Enabled` → `HTTP · Metricool Schedule Post`
- `Filter · API Enabled` → `Airtable · Save Dry Run Post Pack`
- `HTTP · Metricool Schedule Post` → `Code · Aggregate Schedule Results`
- `Code · Aggregate Schedule Results` → `Filter · Schedule OK`
- `Filter · Schedule OK` → `Airtable · Mark Scheduled`
- `Filter · Schedule OK` → `Airtable · Log Schedule Error`
- `Airtable · Mark Scheduled` → `Batch · Split Records`
- `Airtable · Log Schedule Error` → `Batch · Split Records`
- `Airtable · Save Dry Run Post Pack` → `Batch · Split Records`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
