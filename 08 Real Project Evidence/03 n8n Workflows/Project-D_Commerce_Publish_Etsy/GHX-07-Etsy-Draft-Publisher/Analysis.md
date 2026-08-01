# Analysis — GHX-07-Etsy-Draft-Publisher

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-07-Etsy-Draft-Publisher.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Etsy Draft Run | scheduleTrigger | Schedule |
| Set · Load Env Config | set | Set |
| Code · Setup Config | code | Code |
| Airtable · Search Publish Queue | airtable | search |
| Batch · Split Records | splitInBatches | Batch |
| Code · Build Etsy Payload | code | Code |
| Filter · Preflight OK | if | IF |
| HTTP · Etsy Create Draft | httpRequest | HTTP, Etsy |
| Code · Parse Listing Id | code | Code |
| Filter · Listing Created | if | IF |
| HTTP · Download Mockup | httpRequest | HTTP |
| HTTP · Etsy Upload Image | httpRequest | HTTP, Etsy |
| HTTP · Download Digital File | httpRequest | HTTP |
| HTTP · Etsy Upload Digital File | httpRequest | HTTP, Etsy |
| Code · Build Success Payload | code | Code |
| Airtable · Save Etsy Draft | airtable | update |
| Airtable · Log Etsy Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Etsy Draft Run` → `Set · Load Env Config`
- `Set · Load Env Config` → `Code · Setup Config`
- `Code · Setup Config` → `Airtable · Search Publish Queue`
- `Airtable · Search Publish Queue` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build Etsy Payload`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Build Etsy Payload` → `Filter · Preflight OK`
- `Filter · Preflight OK` → `HTTP · Etsy Create Draft`
- `Filter · Preflight OK` → `Airtable · Log Etsy Error`
- `HTTP · Etsy Create Draft` → `Code · Parse Listing Id`
- `Code · Parse Listing Id` → `Filter · Listing Created`
- `Filter · Listing Created` → `HTTP · Download Mockup`
- `Filter · Listing Created` → `Airtable · Log Etsy Error`
- `HTTP · Download Mockup` → `HTTP · Etsy Upload Image`
- `HTTP · Etsy Upload Image` → `HTTP · Download Digital File`
- `HTTP · Download Digital File` → `HTTP · Etsy Upload Digital File`
- `HTTP · Etsy Upload Digital File` → `Code · Build Success Payload`
- `Code · Build Success Payload` → `Airtable · Save Etsy Draft`
- `Airtable · Save Etsy Draft` → `Batch · Split Records`
- `Airtable · Log Etsy Error` → `Batch · Split Records`

## Integration summary
Airtable, Code, Etsy (via HTTP), HTTP Request, IF, Schedule Trigger, Set, Split In Batches

## AI summary
None detected in definition

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
