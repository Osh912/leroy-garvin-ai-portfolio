# Analysis — GHX-12-Content-Idea-Generator

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-12-Content-Idea-Generator.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Daily Content Ideas | scheduleTrigger | Schedule |
| Set · Load Content Niches | set | Set |
| Code · Setup Config | code | Code |
| Airtable · Search Promotable Products | airtable | search |
| Code · Build Daily Ideas Body | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP, OpenAI Chat |
| Code · Parse Content Ideas | code | Code |
| Batch · Split Ideas | splitInBatches | Batch |
| Filter · Idea OK | if | IF |
| Airtable · Create Content Row | airtable | create |
| Code · Log Skip | code | Code |
| Code · Run Complete | code | Code |

## Connections
- `Schedule · Daily Content Ideas` → `Set · Load Content Niches`
- `Set · Load Content Niches` → `Code · Setup Config`
- `Code · Setup Config` → `Airtable · Search Promotable Products`
- `Airtable · Search Promotable Products` → `Code · Build Daily Ideas Body`
- `Code · Build Daily Ideas Body` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Parse Content Ideas`
- `Code · Parse Content Ideas` → `Batch · Split Ideas`
- `Batch · Split Ideas` → `Filter · Idea OK`
- `Batch · Split Ideas` → `Code · Run Complete`
- `Filter · Idea OK` → `Airtable · Create Content Row`
- `Filter · Idea OK` → `Code · Log Skip`
- `Airtable · Create Content Row` → `Batch · Split Ideas`
- `Code · Log Skip` → `Batch · Split Ideas`

## Integration summary
Airtable, Code, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger, Set, Split In Batches

## AI summary
HTTP · OpenAI Chat → OpenAI Chat

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
