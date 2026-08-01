# Analysis — GHX-04-Mockup-Generator

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-04-Mockup-Generator.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Mockup Run | scheduleTrigger | Schedule |
| Airtable · Search Mockup Queue | airtable | search |
| Batch · Split Records | splitInBatches | Batch |
| Code · Build Mockup Chat Body | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP, OpenAI Chat |
| Code · Parse Mockup Prompt | code | Code |
| Filter · Prompt OK | if | IF |
| HTTP · OpenAI Images | httpRequest | HTTP, OpenAI Images |
| Code · Image To Binary | code | Code |
| Filter · Image OK | if | IF |
| Google Drive · Upload Mockup | googleDrive | upload |
| Code · Merge Drive Link | code | Code |
| Airtable · Update Success | airtable | update |
| Airtable · Update Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Mockup Run` → `Airtable · Search Mockup Queue`
- `Airtable · Search Mockup Queue` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build Mockup Chat Body`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Build Mockup Chat Body` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Parse Mockup Prompt`
- `Code · Parse Mockup Prompt` → `Filter · Prompt OK`
- `Filter · Prompt OK` → `HTTP · OpenAI Images`
- `Filter · Prompt OK` → `Airtable · Update Error`
- `HTTP · OpenAI Images` → `Code · Image To Binary`
- `Code · Image To Binary` → `Filter · Image OK`
- `Filter · Image OK` → `Google Drive · Upload Mockup`
- `Filter · Image OK` → `Airtable · Update Error`
- `Google Drive · Upload Mockup` → `Code · Merge Drive Link`
- `Code · Merge Drive Link` → `Airtable · Update Success`
- `Airtable · Update Success` → `Batch · Split Records`
- `Airtable · Update Error` → `Batch · Split Records`

## Integration summary
Airtable, Code, Google Drive, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger, Split In Batches

## AI summary
HTTP · OpenAI Chat → OpenAI Chat, HTTP · OpenAI Images → OpenAI Images

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
