# GHX-14-Metricool-Content-Scheduler

**Portfolio group:** E — Social Scheduling (Metricool)  
**Definition source:** `GHX-14-Metricool-Content-Scheduler.json` (Desktop GH-X workflows export)  
**Complexity:** Advanced  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, process content queue rows, schedule via Metricool HTTP, and save post packs or errors in Airtable.

**Plain English:** Starts on a schedule (`Schedule · Metricool Content Run`). Sets fields (`Set · Load Metricool Config`). Transforms/prepares data in Code node `Code · Setup Config`. Airtable `search` via `Airtable · Search Content Queue`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build Metricool Pack Body`. Transforms/prepares data in Code node `Code · Batch Complete`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Expand Metricool Posts`. Branches with an IF check (`Filter · Pack OK`). Branches with an IF check (`Filter · API Enabled`). Airtable `update` via `Airtable · Log Scheduler Error`. HTTP request via `HTTP · Metricool Schedule Post`. Airtable `update` via `Airtable · Save Post Pack`. Transforms/prepares data in Code node `Code · Aggregate Metricool Results`. Branches with an IF check (`Filter · Schedule OK`).

## Business purpose
On a schedule, process content queue rows, schedule via Metricool HTTP, and save post packs or errors in Airtable.

## What exists in the definition
- **Nodes:** 16 (excluding sticky notes)
- **Connections:** 19
- **Triggers:** Schedule · Metricool Content Run

## Integrations (from nodes)
- Airtable
- Code
- HTTP Request
- IF
- Metricool (via HTTP)
- OpenAI (via HTTP)
- Schedule Trigger
- Set
- Split In Batches

## AI components (from nodes)
- HTTP · OpenAI Chat → OpenAI Chat

## Inputs / outputs (definition-level)
- **Inputs:** Trigger event + Airtable search/filter rows where present
- **Outputs:** Airtable create/update operations and/or external HTTP calls listed above
- **Needs Review:** Exact Airtable base/table names and field schemas (not copied into portfolio to avoid leaking workspace specifics without privacy review)

## Complexity rationale
Estimated **Advanced** from node count (16), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
