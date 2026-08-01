# Analysis — GHX-11-Winning-Idea-Loop

## Source
- File: `/Users/gh-x/Desktop/GH-X/workflows/GHX-11-Winning-Idea-Loop.json`
- Analyzed from workflow **definition** only
- Execution history: **empty / not found** for this export set in local n8n DB

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Weekly Idea Loop | scheduleTrigger | Schedule |
| Airtable · Search Top Winners | airtable | search |
| Code · Build Winner Analysis | code | Code |
| Filter · Has Winners | if | IF |
| HTTP · OpenAI Ideas | httpRequest | HTTP, OpenAI Chat |
| Code · Parse New Ideas | code | Code |
| Airtable · Create Idea Rows | airtable | create |
| Code · Run Complete | code | Code |
| No Op · No Winners | noOp | NoOp |

## Connections
- `Schedule · Weekly Idea Loop` → `Airtable · Search Top Winners`
- `Airtable · Search Top Winners` → `Code · Build Winner Analysis`
- `Code · Build Winner Analysis` → `Filter · Has Winners`
- `Filter · Has Winners` → `HTTP · OpenAI Ideas`
- `Filter · Has Winners` → `No Op · No Winners`
- `HTTP · OpenAI Ideas` → `Code · Parse New Ideas`
- `Code · Parse New Ideas` → `Airtable · Create Idea Rows`
- `Airtable · Create Idea Rows` → `Code · Run Complete`

## Integration summary
Airtable, Code, HTTP Request, IF, NoOp, OpenAI (via HTTP), Schedule Trigger

## AI summary
HTTP · OpenAI Ideas → OpenAI Chat

## Do not claim
- Successful production runs
- Business KPIs, revenue, order volume, or engagement metrics
- That schedules are currently live (`active: false` in export)
