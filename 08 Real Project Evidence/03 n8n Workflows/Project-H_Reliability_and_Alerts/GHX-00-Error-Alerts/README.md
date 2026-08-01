# GHX-00-Error-Alerts

**Portfolio group:** H — Reliability & Alerts  
**Definition source:** `GHX-00-Error-Alerts.json` (Desktop GH-X workflows export)  
**Complexity:** Beginner  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
Catch n8n workflow errors and route them through filtering/alerting logic.

**Plain English:** Starts when another workflow errors (`Error Trigger`). Transforms/prepares data in Code node `Code · Format Payload`. Branches with an IF check (`Filter · Webhook URL Set`). HTTP request via `HTTP · POST Alert`. No-op placeholder (`No Op · Skip Alert`).

## Business purpose
Catch n8n workflow errors and route them through filtering/alerting logic.

## What exists in the definition
- **Nodes:** 5 (excluding sticky notes)
- **Connections:** 4
- **Triggers:** Error Trigger

## Integrations (from nodes)
- Code
- Error Trigger
- HTTP Request
- IF
- NoOp

## AI components (from nodes)
- None detected in node types/HTTP targets (Needs Review if prompts imply external AI elsewhere)

## Inputs / outputs (definition-level)
- **Inputs:** Trigger event + Airtable search/filter rows where present
- **Outputs:** Airtable create/update operations and/or external HTTP calls listed above
- **Needs Review:** Exact Airtable base/table names and field schemas (not copied into portfolio to avoid leaking workspace specifics without privacy review)

## Complexity rationale
Estimated **Beginner** from node count (5), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
