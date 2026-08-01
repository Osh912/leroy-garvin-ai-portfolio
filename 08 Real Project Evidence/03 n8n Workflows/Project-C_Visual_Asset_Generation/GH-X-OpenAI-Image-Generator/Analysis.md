# Analysis — GH-X OpenAI Image Generator

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GH-X OpenAI Image Generator.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Cover Image Run | scheduleTrigger | Schedule |
| Airtable · Search One Ready To Design | airtable | search |
| Code · Build OpenAI Image Body | code | Code |
| HTTP · OpenAI Images | httpRequest | HTTP, OpenAI Images |
| Code · Response To Binary | code | Code |
| Filter · Image OK | if | IF |
| Google Drive · Upload Cover | googleDrive | upload |
| Code · Merge Drive URL | code | Code |
| Airtable · Update By Record Id | airtable | update |
| Airtable · Log Error | airtable | update |

## Connections
- `Schedule · Cover Image Run` → `Airtable · Search One Ready To Design`
- `Airtable · Search One Ready To Design` → `Code · Build OpenAI Image Body`
- `Code · Build OpenAI Image Body` → `HTTP · OpenAI Images`
- `HTTP · OpenAI Images` → `Code · Response To Binary`
- `Code · Response To Binary` → `Filter · Image OK`
- `Filter · Image OK` → `Google Drive · Upload Cover`
- `Filter · Image OK` → `Airtable · Log Error`
- `Google Drive · Upload Cover` → `Code · Merge Drive URL`
- `Code · Merge Drive URL` → `Airtable · Update By Record Id`

## Integration summary
Airtable, Code, Google Drive, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger

## AI summary
HTTP · OpenAI Images → OpenAI Images

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
