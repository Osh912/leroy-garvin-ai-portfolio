# Analysis — GHX-08-Metricool-Scheduler

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-08-Metricool-Scheduler.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Social Schedule Run | scheduleTrigger | Schedule |
| Set · Load Metricool Config | set | Set |
| Code · Setup Config | code | Code |
| Airtable · Search Social Queue | airtable | search |
| Batch · Split Records | splitInBatches | Batch |
| Code · Build Caption Body | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP, OpenAI Chat |
| Code · Expand Platform Posts | code | Code |
| Filter · API Enabled | if | IF |
| HTTP · Metricool Schedule Post | httpRequest | HTTP, Metricool |
| Code · Aggregate Schedule Results | code | Code |
| Filter · Schedule OK | if | IF |
| Airtable · Mark Scheduled | airtable | update |
| Airtable · Log Schedule Error | airtable | update |
| Airtable · Save Dry Run Post Pack | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Social Schedule Run` → `Set · Load Metricool Config`
- `Set · Load Metricool Config` → `Code · Setup Config`
- `Code · Setup Config` → `Airtable · Search Social Queue`
- `Airtable · Search Social Queue` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build Caption Body`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Build Caption Body` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Expand Platform Posts`
- `Code · Expand Platform Posts` → `Filter · API Enabled`
- `Filter · API Enabled` → `HTTP · Metricool Schedule Post`
- `Filter · API Enabled` → `Airtable · Save Dry Run Post Pack`
- `HTTP · Metricool Schedule Post` → `Code · Aggregate Schedule Results`
- `Code · Aggregate Schedule Results` → `Filter · Schedule OK`
- `Filter · Schedule OK` → `Airtable · Mark Scheduled`
- `Filter · Schedule OK` → `Airtable · Log Schedule Error`
- `Airtable · Mark Scheduled` → `Batch · Split Records`
- `Airtable · Log Schedule Error` → `Batch · Split Records`
- `Airtable · Save Dry Run Post Pack` → `Batch · Split Records`

## Integration summary
Airtable, Code, HTTP Request, IF, Metricool (via HTTP), OpenAI (via HTTP), Schedule Trigger, Set, Split In Batches

## AI summary
HTTP · OpenAI Chat → OpenAI Chat

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
