# Analysis — GHX-Generate-Product-Listing

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-Generate-Product-Listing.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Listing Run | scheduleTrigger | Schedule |
| Airtable · Search Ideas | airtable | search |
| Batch · Split Records | splitInBatches | Batch |
| Code · Build Chat Payload | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP, OpenAI Chat |
| Code · Parse Listing JSON | code | Code |
| Filter · Parse OK | if | IF |
| Airtable · Update Success | airtable | update |
| Airtable · Update Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Listing Run` → `Airtable · Search Ideas`
- `Airtable · Search Ideas` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build Chat Payload`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Build Chat Payload` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Parse Listing JSON`
- `Code · Parse Listing JSON` → `Filter · Parse OK`
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
