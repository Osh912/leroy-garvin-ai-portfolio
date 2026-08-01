# Analysis — Design + Reel Prompt Generator

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/Design + Reel Prompt Generator.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule Trigger | scheduleTrigger | Schedule |
| Search records | airtable | search |
| Loop Over Items | splitInBatches | Batch |
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

## Integration summary
Airtable, Code, Schedule Trigger, Split In Batches

## AI summary
None detected in definition

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
