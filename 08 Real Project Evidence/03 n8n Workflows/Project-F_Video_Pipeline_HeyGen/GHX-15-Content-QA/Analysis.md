# Analysis — GHX-15-Content-QA

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-15-Content-QA.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Content QA Sweep | scheduleTrigger | Schedule |
| Airtable · Search QA Queue | airtable | search |
| Batch · Split Records | splitInBatches | Batch |
| Code · Validate Content Fields | code | Code |
| Filter · Content Complete | if | IF |
| Airtable · Mark Video Ready | airtable | update |
| Airtable · Mark Needs Fix | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Content QA Sweep` → `Airtable · Search QA Queue`
- `Airtable · Search QA Queue` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Validate Content Fields`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Validate Content Fields` → `Filter · Content Complete`
- `Filter · Content Complete` → `Airtable · Mark Video Ready`
- `Filter · Content Complete` → `Airtable · Mark Needs Fix`
- `Airtable · Mark Video Ready` → `Batch · Split Records`
- `Airtable · Mark Needs Fix` → `Batch · Split Records`

## Integration summary
Airtable, Code, IF, Schedule Trigger, Split In Batches

## AI summary
None detected in definition

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
