# GHX-07-Performance-Tracker

**Portfolio group:** G — Performance Feedback  
**Definition source:** `GHX-07-Performance-Tracker.json` (Desktop GH-X workflows export)  
**Complexity:** Intermediate  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, review published rows, generate notes via OpenAI HTTP, and save metrics in Airtable.

**Plain English:** Starts on a schedule (`Schedule · Weekly Performance`). Airtable `search` via `Airtable · Search Published`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Score Metrics`. Transforms/prepares data in Code node `Code · Batch Complete`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Merge AI Notes`. Airtable `update` via `Airtable · Save Metrics`.

## Business purpose
On a schedule, review published rows, generate notes via OpenAI HTTP, and save metrics in Airtable.

## What exists in the definition
- **Nodes:** 8 (excluding sticky notes)
- **Connections:** 8
- **Triggers:** Schedule · Weekly Performance

## Integrations (from nodes)
- Airtable
- Code
- HTTP Request
- OpenAI (via HTTP)
- Schedule Trigger
- Split In Batches

## AI components (from nodes)
- HTTP · OpenAI Chat → OpenAI Chat

## Inputs / outputs (definition-level)
- **Inputs:** Trigger event + Airtable search/filter rows where present
- **Outputs:** Airtable create/update operations and/or external HTTP calls listed above
- **Needs Review:** Exact Airtable base/table names and field schemas (not copied into portfolio to avoid leaking workspace specifics without privacy review)

## Complexity rationale
Estimated **Intermediate** from node count (8), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
