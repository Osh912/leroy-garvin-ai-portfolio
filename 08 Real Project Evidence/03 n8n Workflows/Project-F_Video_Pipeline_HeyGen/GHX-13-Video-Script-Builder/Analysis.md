# Analysis — GHX-13-Video-Script-Builder

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-13-Video-Script-Builder.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Script Build Run | scheduleTrigger | Schedule |
| Airtable · Search Script Queue | airtable | search |
| Batch · Split Records | splitInBatches | Batch |
| Code · Build Script Body | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP, OpenAI Chat |
| Code · Parse Platform Scripts | code | Code |
| Filter · Script OK | if | IF |
| Airtable · Save Scripts | airtable | update |
| Airtable · Log Script Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Script Build Run` → `Airtable · Search Script Queue`
- `Airtable · Search Script Queue` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build Script Body`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Build Script Body` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Parse Platform Scripts`
- `Code · Parse Platform Scripts` → `Filter · Script OK`
- `Filter · Script OK` → `Airtable · Save Scripts`
- `Filter · Script OK` → `Airtable · Log Script Error`
- `Airtable · Save Scripts` → `Batch · Split Records`
- `Airtable · Log Script Error` → `Batch · Split Records`

## Integration summary
Airtable, Code, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger, Split In Batches

## AI summary
HTTP · OpenAI Chat → OpenAI Chat

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
