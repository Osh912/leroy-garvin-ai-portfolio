# GHX-08-Metricool-Scheduler

**Portfolio group:** E — Social Scheduling (Metricool)  
**Definition source:** `GHX-08-Metricool-Scheduler.json` (Desktop GH-X workflows export)  
**Complexity:** Advanced  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, build social posts (OpenAI + Metricool HTTP) and mark scheduled / log errors / save dry-run packs in Airtable.

**Plain English:** Starts on a schedule (`Schedule · Social Schedule Run`). Sets fields (`Set · Load Metricool Config`). Transforms/prepares data in Code node `Code · Setup Config`. Airtable `search` via `Airtable · Search Social Queue`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build Caption Body`. Transforms/prepares data in Code node `Code · Batch Complete`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Expand Platform Posts`. Branches with an IF check (`Filter · API Enabled`). HTTP request via `HTTP · Metricool Schedule Post`. Airtable `update` via `Airtable · Save Dry Run Post Pack`. Transforms/prepares data in Code node `Code · Aggregate Schedule Results`. Branches with an IF check (`Filter · Schedule OK`). Airtable `update` via `Airtable · Mark Scheduled`. Airtable `update` via `Airtable · Log Schedule Error`.

## Business purpose
On a schedule, build social posts (OpenAI + Metricool HTTP) and mark scheduled / log errors / save dry-run packs in Airtable.

## What exists in the definition
- **Nodes:** 16 (excluding sticky notes)
- **Connections:** 18
- **Triggers:** Schedule · Social Schedule Run

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
