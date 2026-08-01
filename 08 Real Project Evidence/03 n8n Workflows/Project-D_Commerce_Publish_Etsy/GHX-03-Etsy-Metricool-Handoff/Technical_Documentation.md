# Technical Documentation — GHX-03-Etsy-Metricool-Handoff

## Overview
Prepare publishing handoff fields for Etsy/Metricool-related draft rows in Airtable.

| Field | Value |
|-------|-------|
| Export file | `GHX-03-Etsy-Metricool-Handoff.json` |
| Active in export | `False` |
| Nodes / connections | 4 / 3 |
| Complexity | Beginner |
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
| Schedule · Publishing Prep | scheduleTrigger | Schedule |
| Airtable · Search Ready Rows | airtable | search |
| Code · Build Draft JSON | code | Code |
| Airtable · Save Drafts | airtable | update |

## Connections
- `Schedule · Publishing Prep` → `Airtable · Search Ready Rows`
- `Airtable · Search Ready Rows` → `Code · Build Draft JSON`
- `Code · Build Draft JSON` → `Airtable · Save Drafts`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
