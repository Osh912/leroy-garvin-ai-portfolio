# Technical Documentation — Design + Reel Prompt Generator

## Overview
Build design and reel prompts in Code nodes and write them back to Airtable on a schedule.

| Field | Value |
|-------|-------|
| Export file | `Design + Reel Prompt Generator.json` |
| Active in export | `False` |
| Nodes / connections | 6 / 6 |
| Complexity | Intermediate |
| Status | Functional Build (not Production Ready) |

## Services & integrations
- Airtable
- n8n Code
- n8n Schedule Trigger

## AI / APIs
- None detected in definition


**Needs Review:** Exact model IDs and secrets are not published.

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule Trigger | scheduleTrigger | Schedule |
| Search records | airtable | search |
| Loop Over Items | splitInBatches | — |
| Batch complete | code | Code |
| Code in JavaScript | code | Code |
| Update record | airtable | update |

## Connections
- `Schedule Trigger` → `Search records`
- `Search records` → `Loop Over Items`
- `Loop Over Items` → `Code in JavaScript`
- `Loop Over Items` → `Batch complete`
- `Code in JavaScript` → `Update record`
- `Update record` → `Loop Over Items`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
