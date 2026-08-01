# Analysis — GHX-14-Metricool-Content-Scheduler

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-14-Metricool-Content-Scheduler.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Metricool Content Run | scheduleTrigger | Schedule |
| Set · Load Metricool Config | set | Set |
| Code · Setup Config | code | Code |
| Airtable · Search Content Queue | airtable | search |
| Batch · Split Records | splitInBatches | Batch |
| Code · Build Metricool Pack Body | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP, OpenAI Chat |
| Code · Expand Metricool Posts | code | Code |
| Filter · Pack OK | if | IF |
| Filter · API Enabled | if | IF |
| HTTP · Metricool Schedule Post | httpRequest | HTTP, Metricool |
| Code · Aggregate Metricool Results | code | Code |
| Filter · Schedule OK | if | IF |
| Airtable · Save Post Pack | airtable | update |
| Airtable · Log Scheduler Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Metricool Content Run` → `Set · Load Metricool Config`
- `Set · Load Metricool Config` → `Code · Setup Config`
- `Code · Setup Config` → `Airtable · Search Content Queue`
- `Airtable · Search Content Queue` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build Metricool Pack Body`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Build Metricool Pack Body` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Expand Metricool Posts`
- `Code · Expand Metricool Posts` → `Filter · Pack OK`
- `Filter · Pack OK` → `Filter · API Enabled`
- `Filter · Pack OK` → `Airtable · Log Scheduler Error`
- `Filter · API Enabled` → `HTTP · Metricool Schedule Post`
- `Filter · API Enabled` → `Airtable · Save Post Pack`
- `HTTP · Metricool Schedule Post` → `Code · Aggregate Metricool Results`
- `Code · Aggregate Metricool Results` → `Filter · Schedule OK`
- `Filter · Schedule OK` → `Airtable · Save Post Pack`
- `Filter · Schedule OK` → `Airtable · Log Scheduler Error`
- `Airtable · Save Post Pack` → `Batch · Split Records`
- `Airtable · Log Scheduler Error` → `Batch · Split Records`

## Integration summary
Airtable, Code, HTTP Request, IF, Metricool (via HTTP), OpenAI (via HTTP), Schedule Trigger, Set, Split In Batches

## AI summary
HTTP · OpenAI Chat → OpenAI Chat

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
