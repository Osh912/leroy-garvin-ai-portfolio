# Technical Documentation — GHX-01-Idea-Intelligence

## Overview
Create new product idea records in Airtable using scheduled OpenAI chat calls.

| Field | Value |
|-------|-------|
| Export file | `GHX-01-Idea-Intelligence.json` |
| Active in export | `False` |
| Nodes / connections | 5 / 4 |
| Complexity | Beginner |
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
| Schedule · Weekly Ideas | scheduleTrigger | Schedule |
| Code · Build OpenAI Body | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP |
| Code · Parse Ideas | code | Code |
| Airtable · Create Product | airtable | create |

## Connections
- `Schedule · Weekly Ideas` → `Code · Build OpenAI Body`
- `Code · Build OpenAI Body` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Parse Ideas`
- `Code · Parse Ideas` → `Airtable · Create Product`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
