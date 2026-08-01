# Technical Documentation — GHX-07-Etsy-Draft-Publisher

## Overview
Create Etsy draft listings and upload images/digital files via Etsy HTTP APIs; save results to Airtable.

| Field | Value |
|-------|-------|
| Export file | `GHX-07-Etsy-Draft-Publisher.json` |
| Active in export | `False` |
| Nodes / connections | 18 / 20 |
| Complexity | Advanced |
| Status | Functional Build (not Production Ready) |

## Services & integrations
- Airtable
- Etsy API
- HTTP Request
- n8n Code
- n8n Schedule Trigger

## AI / APIs
- None detected in definition


**Needs Review:** Exact model IDs and secrets are not published.

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Schedule · Etsy Draft Run | scheduleTrigger | Schedule |
| Set · Load Env Config | set | — |
| Code · Setup Config | code | Code |
| Airtable · Search Publish Queue | airtable | search |
| Batch · Split Records | splitInBatches | — |
| Code · Build Etsy Payload | code | Code |
| Filter · Preflight OK | if | — |
| HTTP · Etsy Create Draft | httpRequest | HTTP |
| Code · Parse Listing Id | code | Code |
| Filter · Listing Created | if | — |
| HTTP · Download Mockup | httpRequest | HTTP |
| HTTP · Etsy Upload Image | httpRequest | HTTP |
| HTTP · Download Digital File | httpRequest | HTTP |
| HTTP · Etsy Upload Digital File | httpRequest | HTTP |
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

## Non-claims
No execution history, production usage, revenue, or customer metrics.
