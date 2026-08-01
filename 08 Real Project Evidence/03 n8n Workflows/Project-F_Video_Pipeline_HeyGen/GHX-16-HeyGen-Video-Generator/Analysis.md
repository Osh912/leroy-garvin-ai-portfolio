# Analysis — GHX-16-HeyGen-Video-Generator

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-16-HeyGen-Video-Generator.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Every 15 Minutes | scheduleTrigger | Schedule |
| Set · Load HeyGen Config | set | Set |
| Code · Setup Config | code | Code |
| Airtable · Search Video Ready | airtable | search |
| Batch · Split Records | splitInBatches | Batch |
| Code · Build HeyGen Payload | code | Code |
| Filter · Payload OK | if | IF |
| HTTP · HeyGen Create Video | httpRequest | HTTP, HeyGen |
| Code · Parse HeyGen Response | code | Code |
| Filter · Video Id Returned | if | IF |
| Airtable · Mark Video Processing | airtable | update |
| Airtable · Log HeyGen Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Every 15 Minutes` → `Set · Load HeyGen Config`
- `Set · Load HeyGen Config` → `Code · Setup Config`
- `Code · Setup Config` → `Airtable · Search Video Ready`
- `Airtable · Search Video Ready` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build HeyGen Payload`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Build HeyGen Payload` → `Filter · Payload OK`
- `Filter · Payload OK` → `HTTP · HeyGen Create Video`
- `Filter · Payload OK` → `Airtable · Log HeyGen Error`
- `HTTP · HeyGen Create Video` → `Code · Parse HeyGen Response`
- `Code · Parse HeyGen Response` → `Filter · Video Id Returned`
- `Filter · Video Id Returned` → `Airtable · Mark Video Processing`
- `Filter · Video Id Returned` → `Airtable · Log HeyGen Error`
- `Airtable · Mark Video Processing` → `Batch · Split Records`
- `Airtable · Log HeyGen Error` → `Batch · Split Records`

## Integration summary
Airtable, Code, HTTP Request, HeyGen (via HTTP), IF, Schedule Trigger, Set, Split In Batches

## AI summary
HTTP · HeyGen Create Video → HeyGen

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
