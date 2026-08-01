# Analysis — GHX-09-Self-Healing-QA

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-09-Self-Healing-QA.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · QA Sweep | scheduleTrigger | Schedule |
| Airtable · Search Failed Rows | airtable | search |
| Batch · Split Records | splitInBatches | Batch |
| Code · Classify Failure | code | Code |
| Filter · Can Auto Retry | if | IF |
| Airtable · Requeue For Retry | airtable | update |
| Airtable · Flag Manual Review | airtable | update |
| Filter · Webhook Set | if | IF |
| HTTP · Admin Alert | httpRequest | HTTP |
| No Op · Skip Alert | noOp | NoOp |
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

## Integration summary
Airtable, Code, HTTP Request, IF, NoOp, Schedule Trigger, Split In Batches

## AI summary
None detected in definition

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
