# Analysis — GHX-06-Publish-Queue-Manager

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-06-Publish-Queue-Manager.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Validation Run | scheduleTrigger | Schedule |
| Airtable · Search Ready To Publish | airtable | search |
| Batch · Split Records | splitInBatches | Batch |
| Code · Validate Publish Gate | code | Code |
| Filter · Complete | if | IF |
| Airtable · Mark Publish Ready | airtable | update |
| Airtable · Append Error Log | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Validation Run` → `Airtable · Search Ready To Publish`
- `Airtable · Search Ready To Publish` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Validate Publish Gate`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Validate Publish Gate` → `Filter · Complete`
- `Filter · Complete` → `Airtable · Mark Publish Ready`
- `Filter · Complete` → `Airtable · Append Error Log`
- `Airtable · Mark Publish Ready` → `Batch · Split Records`
- `Airtable · Append Error Log` → `Batch · Split Records`

## Integration summary
Airtable, Code, IF, Schedule Trigger, Split In Batches

## AI summary
None detected in definition

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
