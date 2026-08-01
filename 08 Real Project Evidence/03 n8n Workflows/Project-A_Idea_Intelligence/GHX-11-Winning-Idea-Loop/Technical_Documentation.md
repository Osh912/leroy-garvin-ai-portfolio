# Technical Documentation — GHX-11-Winning-Idea-Loop

## Overview
Use stronger-performing records to generate new idea rows via OpenAI and Airtable.

| Field | Value |
|-------|-------|
| Export file | `GHX-11-Winning-Idea-Loop.json` |
| Active in export | `False` |
| Nodes / connections | 9 / 8 |
| Complexity | Intermediate |
| Status | Functional Build (not Production Ready) |

## Services & integrations
- Airtable
- HTTP Request
- OpenAI API
- n8n Code
- n8n Schedule Trigger

## AI / APIs
- HTTP · OpenAI Ideas → OpenAI Chat Completions API
- OpenAI Chat Completions API

**Needs Review:** Exact model IDs and secrets are not published.

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Weekly Idea Loop | scheduleTrigger | Schedule |
| Airtable · Search Top Winners | airtable | search |
| Code · Build Winner Analysis | code | Code |
| Filter · Has Winners | if | — |
| HTTP · OpenAI Ideas | httpRequest | HTTP |
| Code · Parse New Ideas | code | Code |
| Airtable · Create Idea Rows | airtable | create |
| Code · Run Complete | code | Code |
| No Op · No Winners | noOp | — |

## Connections
- `Schedule · Weekly Idea Loop` → `Airtable · Search Top Winners`
- `Airtable · Search Top Winners` → `Code · Build Winner Analysis`
- `Code · Build Winner Analysis` → `Filter · Has Winners`
- `Filter · Has Winners` → `HTTP · OpenAI Ideas`
- `Filter · Has Winners` → `No Op · No Winners`
- `HTTP · OpenAI Ideas` → `Code · Parse New Ideas`
- `Code · Parse New Ideas` → `Airtable · Create Idea Rows`
- `Airtable · Create Idea Rows` → `Code · Run Complete`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
