# Technical Documentation — GH-X OpenAI Image Generator

## Overview
Generate cover/product images via OpenAI Images, store via Google Drive, update Airtable.

| Field | Value |
|-------|-------|
| Export file | `GH-X OpenAI Image Generator.json` |
| Active in export | `False` |
| Nodes / connections | 10 / 9 |
| Complexity | Intermediate |
| Status | Functional Build (not Production Ready) |

## Services & integrations
- Airtable
- Google Drive
- HTTP Request
- OpenAI API
- n8n Code
- n8n Schedule Trigger

## AI / APIs
- HTTP · OpenAI Images → OpenAI Images API
- OpenAI Images API

**Needs Review:** Exact model IDs and secrets are not published.

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Cover Image Run | scheduleTrigger | Schedule |
| Airtable · Search One Ready To Design | airtable | search |
| Code · Build OpenAI Image Body | code | Code |
| HTTP · OpenAI Images | httpRequest | HTTP |
| Code · Response To Binary | code | Code |
| Filter · Image OK | if | — |
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

## Non-claims
No execution history, production usage, revenue, or customer metrics.
