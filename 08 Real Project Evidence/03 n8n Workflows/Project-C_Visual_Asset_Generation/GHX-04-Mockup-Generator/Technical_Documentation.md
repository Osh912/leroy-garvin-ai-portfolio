# Technical Documentation — GHX-04-Mockup-Generator

## Overview
Generate mockups using OpenAI Chat + Images, store via Google Drive, update Airtable queue rows.

| Field | Value |
|-------|-------|
| Export file | `GHX-04-Mockup-Generator.json` |
| Active in export | `False` |
| Nodes / connections | 15 / 17 |
| Complexity | Advanced |
| Status | Functional Build (not Production Ready) |

## Services & integrations
- Airtable
- Google Drive
- HTTP Request
- OpenAI API
- n8n Code
- n8n Schedule Trigger

## AI / APIs
- HTTP · OpenAI Chat → OpenAI Chat Completions API
- HTTP · OpenAI Images → OpenAI Images API
- OpenAI Chat Completions API
- OpenAI Images API

**Needs Review:** Exact model IDs and secrets are not published.

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Mockup Run | scheduleTrigger | Schedule |
| Airtable · Search Mockup Queue | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Build Mockup Chat Body | code | Code |
| HTTP · OpenAI Chat | httpRequest | HTTP |
| Code · Parse Mockup Prompt | code | Code |
| Filter · Prompt OK | if | — |
| HTTP · OpenAI Images | httpRequest | HTTP |
| Code · Image To Binary | code | Code |
| Filter · Image OK | if | — |
| Google Drive · Upload Mockup | googleDrive | upload |
| Code · Merge Drive Link | code | Code |
| Airtable · Update Success | airtable | update |
| Airtable · Update Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Mockup Run` → `Airtable · Search Mockup Queue`
- `Airtable · Search Mockup Queue` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Build Mockup Chat Body`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Build Mockup Chat Body` → `HTTP · OpenAI Chat`
- `HTTP · OpenAI Chat` → `Code · Parse Mockup Prompt`
- `Code · Parse Mockup Prompt` → `Filter · Prompt OK`
- `Filter · Prompt OK` → `HTTP · OpenAI Images`
- `Filter · Prompt OK` → `Airtable · Update Error`
- `HTTP · OpenAI Images` → `Code · Image To Binary`
- `Code · Image To Binary` → `Filter · Image OK`
- `Filter · Image OK` → `Google Drive · Upload Mockup`
- `Filter · Image OK` → `Airtable · Update Error`
- `Google Drive · Upload Mockup` → `Code · Merge Drive Link`
- `Code · Merge Drive Link` → `Airtable · Update Success`
- `Airtable · Update Success` → `Batch · Split Records`
- `Airtable · Update Error` → `Batch · Split Records`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
