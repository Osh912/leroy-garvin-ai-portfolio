# Analysis — GHX-05-Social-Asset-Generator

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-05-Social-Asset-Generator.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Social Run | scheduleTrigger | Schedule |
| Airtable · Search Social Queue | airtable | search |
| Batch · Split Records | splitInBatches | Batch |
| Code · Build Social Chat Body | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP, OpenAI Chat |
| Code · Parse Social JSON | code | Code |
| Filter · Parse OK | if | IF |
| Airtable · Update Success | airtable | update |
| Airtable · Update Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Social Run` → `Airtable · Search Social Queue`
- `Airtable · Search Social Queue` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build Social Chat Body`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Build Social Chat Body` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Parse Social JSON`
- `Code · Parse Social JSON` → `Filter · Parse OK`
- `Filter · Parse OK` → `Airtable · Update Success`
- `Filter · Parse OK` → `Airtable · Update Error`
- `Airtable · Update Success` → `Batch · Split Records`
- `Airtable · Update Error` → `Batch · Split Records`

## Integration summary
Airtable, Code, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger, Split In Batches

## AI summary
HTTP · OpenAI Chat → OpenAI Chat

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
