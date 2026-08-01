# Analysis — GHX-17-HeyGen-Status-Poller

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-17-HeyGen-Status-Poller.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Every 10 Minutes | scheduleTrigger | Schedule |
| Airtable · Search Processing Videos | airtable | search |
| Batch · Split Records | splitInBatches | Batch |
| Code · Prepare Poll Context | code | Code |
| Filter · Context OK | if | IF |
| HTTP · HeyGen Get Status | httpRequest | HTTP, HeyGen |
| Code · Parse HeyGen Status | code | Code |
| Switch · HeyGen Status | switch | Switch |
| Airtable · Mark Ready To Schedule | airtable | update |
| Code · Log Still Processing | code | Code |
| Airtable · Mark Video Failed | airtable | update |
| Airtable · Log Poll Error | airtable | update |
| Airtable · Log Context Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Every 10 Minutes` → `Airtable · Search Processing Videos`
- `Airtable · Search Processing Videos` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Prepare Poll Context`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Prepare Poll Context` → `Filter · Context OK`
- `Filter · Context OK` → `HTTP · HeyGen Get Status`
- `Filter · Context OK` → `Airtable · Log Context Error`
- `HTTP · HeyGen Get Status` → `Code · Parse HeyGen Status`
- `Code · Parse HeyGen Status` → `Switch · HeyGen Status`
- `Switch · HeyGen Status` → `Airtable · Mark Ready To Schedule`
- `Switch · HeyGen Status` → `Code · Log Still Processing`
- `Switch · HeyGen Status` → `Airtable · Mark Video Failed`
- `Switch · HeyGen Status` → `Airtable · Log Poll Error`
- `Airtable · Mark Ready To Schedule` → `Batch · Split Records`
- `Code · Log Still Processing` → `Batch · Split Records`
- `Airtable · Mark Video Failed` → `Batch · Split Records`
- `Airtable · Log Poll Error` → `Batch · Split Records`
- `Airtable · Log Context Error` → `Batch · Split Records`

## Integration summary
Airtable, Code, HTTP Request, HeyGen (via HTTP), IF, Schedule Trigger, Split In Batches, Switch

## AI summary
HTTP · HeyGen Get Status → HeyGen

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
