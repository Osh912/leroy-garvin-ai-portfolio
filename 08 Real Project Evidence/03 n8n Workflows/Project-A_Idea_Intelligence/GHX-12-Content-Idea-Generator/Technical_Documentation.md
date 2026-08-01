# Technical Documentation — GHX-12-Content-Idea-Generator

## Overview
Generate social/content ideas for promotable products and store them in Airtable.

| Field | Value |
|-------|-------|
| Export file | `GHX-12-Content-Idea-Generator.json` |
| Active in export | `False` |
| Nodes / connections | 12 / 13 |
| Complexity | Intermediate |
| Status | Functional Build (not Production Ready) |

## Services & integrations
- Airtable
- HTTP Request
- OpenAI API
- n8n Code
- n8n Schedule Trigger

## AI / APIs
- HTTP · OpenAI Chat → OpenAI Chat Completions API
- OpenAI Chat Completions API

**Needs Review:** Exact model IDs and secrets are not published.

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Daily Content Ideas | scheduleTrigger | Schedule |
| Set · Load Content Niches | set | — |
| Code · Setup Config | code | Code |
| Airtable · Search Promotable Products | airtable | search |
| Code · Build Daily Ideas Body | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP |
| Code · Parse Content Ideas | code | Code |
| Batch · Split Ideas | splitInBatches | — |
| Filter · Idea OK | if | — |
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

## Non-claims
No execution history, production usage, revenue, or customer metrics.
