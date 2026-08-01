# Technical Documentation — GHX-03B-Product-File-Uploader

## Overview
Create product blueprint/image assets via OpenAI HTTP and write product file URLs or errors to Airtable.

| Field | Value |
|-------|-------|
| Export file | `GHX-03B-Product-File-Uploader.json` |
| Active in export | `False` |
| Nodes / connections | 22 / 29 |
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
- HTTP · OpenAI Product Blueprint → OpenAI Chat Completions API
- HTTP · OpenAI Product Image → OpenAI Images API
- OpenAI Chat Completions API
- OpenAI Images API

**Needs Review:** Exact model IDs and secrets are not published.

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Product File Run | scheduleTrigger | Schedule |
| Set · Load Product Gen Config | set | — |
| Code · Setup Config | code | Code |
| Airtable · Search Needs Product File | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Prepare Product Job | code | Code |
| Filter · Job OK | if | — |
| HTTP · OpenAI Product Blueprint | httpRequest | HTTP |
| Code · Parse Product Blueprint | code | Code |
| Filter · Blueprint OK | if | — |
| Switch · Output Format | switch | — |
| Code · Generate Product File · PDF | code | Code |
| HTTP · OpenAI Product Image | httpRequest | HTTP |
| Code · Image To Binary | code | Code |
| Filter · Image OK | if | — |
| Code · Generate Product File · Visual | code | Code |
| Filter · Product Binary OK | if | — |
| Google Drive · Upload Product File | googleDrive | upload |
| Code · Build Download URL | code | Code |
| Airtable · Write Product File URL | airtable | update |
| Airtable · Log File Error | airtable | update |
| Code · Batch Complete | code | Code |

## Connections
- `Schedule · Product File Run` → `Set · Load Product Gen Config`
- `Set · Load Product Gen Config` → `Code · Setup Config`
- `Code · Setup Config` → `Airtable · Search Needs Product File`
- `Airtable · Search Needs Product File` → `Batch · Split Records`
- `Batch · Split Records` → `Code · Prepare Product Job`
- `Batch · Split Records` → `Code · Batch Complete`
- `Code · Prepare Product Job` → `Filter · Job OK`
- `Filter · Job OK` → `HTTP · OpenAI Product Blueprint`
- `Filter · Job OK` → `Airtable · Log File Error`
- `HTTP · OpenAI Product Blueprint` → `Code · Parse Product Blueprint`
- `Code · Parse Product Blueprint` → `Filter · Blueprint OK`
- `Filter · Blueprint OK` → `Switch · Output Format`
- `Filter · Blueprint OK` → `Airtable · Log File Error`
- `Switch · Output Format` → `Code · Generate Product File · PDF`
- `Switch · Output Format` → `HTTP · OpenAI Product Image`
- `Switch · Output Format` → `HTTP · OpenAI Product Image`
- `Switch · Output Format` → `Airtable · Log File Error`
- `Code · Generate Product File · PDF` → `Filter · Product Binary OK`
- `HTTP · OpenAI Product Image` → `Code · Image To Binary`
- `Code · Image To Binary` → `Filter · Image OK`
- `Filter · Image OK` → `Code · Generate Product File · Visual`
- `Filter · Image OK` → `Airtable · Log File Error`
- `Code · Generate Product File · Visual` → `Filter · Product Binary OK`
- `Filter · Product Binary OK` → `Google Drive · Upload Product File`
- `Filter · Product Binary OK` → `Airtable · Log File Error`
- `Google Drive · Upload Product File` → `Code · Build Download URL`
- `Code · Build Download URL` → `Airtable · Write Product File URL`
- `Airtable · Write Product File URL` → `Batch · Split Records`
- `Airtable · Log File Error` → `Batch · Split Records`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
