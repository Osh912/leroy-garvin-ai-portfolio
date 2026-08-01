# Analysis — GHX-10-Performance-Tracker

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-10-Performance-Tracker.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Weekly Metrics | scheduleTrigger | Schedule |
| Airtable · Search Live Products | airtable | search |
| Batch · Split Records | splitInBatches | Batch |
| Code · Prep Metrics Context | code | Code |
| Filter · Has Etsy Listing | if | IF |
| HTTP · Etsy Get Listing | httpRequest | HTTP, Etsy |
| Code · Score Metrics | code | Code |
| Code · Score Without Etsy | code | Code |
| HTTP · OpenAI Notes | httpRequest | HTTP, OpenAI Chat |
| Code · Merge AI Notes | code | Code |
| Airtable · Save Metrics | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Weekly Metrics` → `Airtable · Search Live Products`
- `Airtable · Search Live Products` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Prep Metrics Context`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Prep Metrics Context` → `Filter · Has Etsy Listing`
- `Filter · Has Etsy Listing` → `HTTP · Etsy Get Listing`
- `Filter · Has Etsy Listing` → `Code · Score Without Etsy`
- `HTTP · Etsy Get Listing` → `Code · Score Metrics`
- `Code · Score Metrics` → `HTTP · OpenAI Notes`
- `Code · Score Without Etsy` → `HTTP · OpenAI Notes`
- `HTTP · OpenAI Notes` → `Code · Merge AI Notes`
- `Code · Merge AI Notes` → `Airtable · Save Metrics`
- `Airtable · Save Metrics` → `Batch · Split Records`

## Integration summary
Airtable, Code, Etsy (via HTTP), HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger, Split In Batches

## AI summary
HTTP · OpenAI Notes → OpenAI Chat

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
