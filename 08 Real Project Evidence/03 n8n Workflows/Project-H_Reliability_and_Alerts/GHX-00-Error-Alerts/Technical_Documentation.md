# Technical Documentation — GHX-00-Error-Alerts

## Overview
Catch n8n workflow errors and route through filter/HTTP alert logic.

| Field | Value |
|-------|-------|
| Export file | `GHX-00-Error-Alerts.json` |
| Active in export | `False` |
| Nodes / connections | 5 / 4 |
| Complexity | Beginner |
| Status | Functional Build (not Production Ready) |

## Services & integrations
- HTTP Request
- n8n Code
- n8n Error Trigger

## AI / APIs
- None detected in definition


**Needs Review:** Exact model IDs and secrets are not published.

## Node inventory
| Node | Type | Notes |
|------|------|-------|
| Error Trigger | errorTrigger | Error Trigger |
| Code · Format Payload | code | Code |
| Filter · Webhook URL Set | if | — |
| HTTP · POST Alert | httpRequest | HTTP |
| No Op · Skip Alert | noOp | — |

## Connections
- `Error Trigger` → `Code · Format Payload`
- `Code · Format Payload` → `Filter · Webhook URL Set`
- `Filter · Webhook URL Set` → `HTTP · POST Alert`
- `Filter · Webhook URL Set` → `No Op · Skip Alert`

## Non-claims
No execution history, production usage, revenue, or customer metrics.
