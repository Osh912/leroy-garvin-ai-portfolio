# Analysis — GHX-03-Etsy-Metricool-Handoff

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-03-Etsy-Metricool-Handoff.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

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

## Integration summary
Airtable, Code, Schedule Trigger

## AI summary
None detected in definition

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
