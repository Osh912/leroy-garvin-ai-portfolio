# Analysis — GHX-01-Idea-Intelligence

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-01-Idea-Intelligence.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Weekly Ideas | scheduleTrigger | Schedule |
| Code · Build OpenAI Body | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP, OpenAI Chat |
| Code · Parse Ideas | code | Code |
| Airtable · Create Product | airtable | create |

## Connections
- `Schedule · Weekly Ideas` → `Code · Build OpenAI Body`
- `Code · Build OpenAI Body` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Parse Ideas`
- `Code · Parse Ideas` → `Airtable · Create Product`

## Integration summary
Airtable, Code, HTTP Request, OpenAI (via HTTP), Schedule Trigger

## AI summary
HTTP · OpenAI Chat → OpenAI Chat

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
