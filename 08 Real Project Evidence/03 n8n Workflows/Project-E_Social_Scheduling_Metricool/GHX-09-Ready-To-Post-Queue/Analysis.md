# Analysis — GHX-09-Ready-To-Post-Queue

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-09-Ready-To-Post-Queue.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Every Hour | scheduleTrigger | Schedule |
| Code · Reset Run Counters | code | Code |
| Airtable · Search Scheduled Content | airtable | search |
| Batch · Split Records | splitInBatches | Batch |
| Code · Build Ready-To-Post Queue Items | code | Code |
| Filter · Queue Item OK | if | IF |
| Airtable · Create Ready To Post Row | airtable | create |
| Airtable · Mark Queued To Post | airtable | update |
| Code · Log Queued Item | code | Code |
| Code · Log Skipped Item | code | Code |
| Code · Run Summary | code | Code |

## Connections
- `Schedule · Every Hour` → `Code · Reset Run Counters`
- `Code · Reset Run Counters` → `Airtable · Search Scheduled Content`
- `Airtable · Search Scheduled Content` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build Ready-To-Post Queue Items`
- `Batch · Split Records` → `Code · Run Summary`
- `Code · Build Ready-To-Post Queue Items` → `Filter · Queue Item OK`
- `Filter · Queue Item OK` → `Airtable · Create Ready To Post Row`
- `Filter · Queue Item OK` → `Code · Log Skipped Item`
- `Airtable · Create Ready To Post Row` → `Airtable · Mark Queued To Post`
- `Airtable · Mark Queued To Post` → `Code · Log Queued Item`
- `Code · Log Queued Item` → `Batch · Split Records`
- `Code · Log Skipped Item` → `Batch · Split Records`

## Integration summary
Airtable, Code, IF, Schedule Trigger, Split In Batches

## AI summary
None detected in definition

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
