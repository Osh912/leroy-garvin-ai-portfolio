# Analysis — GHX-07-Performance-Tracker

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-07-Performance-Tracker.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Weekly Performance | scheduleTrigger | Schedule |
| Airtable · Search Published | airtable | search |
| Batch · Split Records | splitInBatches | Batch |
| Code · Score Metrics | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP, OpenAI Chat |
| Code · Merge AI Notes | code | Code |
| Airtable · Save Metrics | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Weekly Performance` → `Airtable · Search Published`
- `Airtable · Search Published` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Score Metrics`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Score Metrics` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Merge AI Notes`
- `Code · Merge AI Notes` → `Airtable · Save Metrics`
- `Airtable · Save Metrics` → `Batch · Split Records`

## Integration summary
Airtable, Code, HTTP Request, OpenAI (via HTTP), Schedule Trigger, Split In Batches

## AI summary
HTTP · OpenAI Chat → OpenAI Chat

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
