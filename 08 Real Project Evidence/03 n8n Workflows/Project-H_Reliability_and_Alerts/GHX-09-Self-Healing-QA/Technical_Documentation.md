# Technical Documentation — GHX-09-Self-Healing-QA

## Overview
Find failed Airtable rows and requeue or flag for manual review.

| Field | Value |
|-------|-------|
| Export file | `GHX-09-Self-Healing-QA.json` |
| Active in export | `False` |
| Nodes / connections | 11 / 13 |
| Complexity | Intermediate |
| Status | Functional Build (not Production Ready) |

## Services & integrations
- Airtable
- HTTP Request
- n8n Code
- n8n Schedule Trigger

## AI / APIs
- None detected in definition


**Needs Review:** Exact model IDs and secrets are not published.

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · QA Sweep | scheduleTrigger | Schedule |
| Airtable · Search Failed Rows | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Classify Failure | code | Code |
| Filter · Can Auto Retry | if | — |
| Airtable · Requeue For Retry | airtable | update |
| Airtable · Flag Manual Review | airtable | update |
| Filter · Webhook Set | if | — |
| HTTP · Admin Alert | httpRequest | HTTP |
| No Op · Skip Alert | noOp | — |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · QA Sweep` → `Airtable · Search Failed Rows`
- `Airtable · Search Failed Rows` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Classify Failure`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Classify Failure` → `Filter · Can Auto Retry`
- `Filter · Can Auto Retry` → `Airtable · Requeue For Retry`
- `Filter · Can Auto Retry` → `Airtable · Flag Manual Review`
- `Airtable · Requeue For Retry` → `Filter · Webhook Set`
- `Airtable · Flag Manual Review` → `Filter · Webhook Set`
- `Filter · Webhook Set` → `HTTP · Admin Alert`
- `Filter · Webhook Set` → `No Op · Skip Alert`
- `HTTP · Admin Alert` → `Batch · Split Records`
- `No Op · Skip Alert` → `Batch · Split Records`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
