# GHX-09-Ready-To-Post-Queue

**Portfolio group:** E — Social Scheduling (Metricool)  
**Definition source:** `GHX-09-Ready-To-Post-Queue.json` (Desktop GH-X workflows export)  
**Complexity:** Intermediate  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, find scheduled content and create ready-to-post queue rows in Airtable.

**Plain English:** Starts on a schedule (`Schedule · Every Hour`). Transforms/prepares data in Code node `Code · Reset Run Counters`. Airtable `search` via `Airtable · Search Scheduled Content`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build Ready-To-Post Queue Items`. Transforms/prepares data in Code node `Code · Run Summary`. Branches with an IF check (`Filter · Queue Item OK`). Airtable `create` via `Airtable · Create Ready To Post Row`. Transforms/prepares data in Code node `Code · Log Skipped Item`. Airtable `update` via `Airtable · Mark Queued To Post`. Transforms/prepares data in Code node `Code · Log Queued Item`.

## Business purpose
On a schedule, find scheduled content and create ready-to-post queue rows in Airtable.

## What exists in the definition
- **Nodes:** 11 (excluding sticky notes)
- **Connections:** 12
- **Triggers:** Schedule · Every Hour

## Integrations (from nodes)
- Airtable
- Code
- IF
- Schedule Trigger
- Split In Batches

## AI components (from nodes)
- None detected in node types/HTTP targets (Needs Review if prompts imply external AI elsewhere)

## Inputs / outputs (definition-level)
- **Inputs:** Trigger event + Airtable search/filter rows where present
- **Outputs:** Airtable create/update operations and/or external HTTP calls listed above
- **Needs Review:** Exact Airtable base/table names and field schemas (not copied into portfolio to avoid leaking workspace specifics without privacy review)

## Complexity rationale
Estimated **Intermediate** from node count (11), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
