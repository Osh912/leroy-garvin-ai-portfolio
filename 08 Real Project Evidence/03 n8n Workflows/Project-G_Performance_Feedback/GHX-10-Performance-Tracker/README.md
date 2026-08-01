# GHX-10-Performance-Tracker

**Portfolio group:** G — Performance Feedback  
**Definition source:** `GHX-10-Performance-Tracker.json` (Desktop GH-X workflows export)  
**Complexity:** Advanced  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, fetch live product metrics (Etsy HTTP + OpenAI notes) and save metrics in Airtable.

**Plain English:** Starts on a schedule (`Schedule · Weekly Metrics`). Airtable `search` via `Airtable · Search Live Products`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Prep Metrics Context`. Transforms/prepares data in Code node `Code · Batch Complete`. Branches with an IF check (`Filter · Has Etsy Listing`). HTTP request via `HTTP · Etsy Get Listing`. Transforms/prepares data in Code node `Code · Score Without Etsy`. Transforms/prepares data in Code node `Code · Score Metrics`. HTTP request via `HTTP · OpenAI Notes` (OpenAI Chat). Transforms/prepares data in Code node `Code · Merge AI Notes`. Airtable `update` via `Airtable · Save Metrics`.

## Business purpose
On a schedule, fetch live product metrics (Etsy HTTP + OpenAI notes) and save metrics in Airtable.

## What exists in the definition
- **Nodes:** 12 (excluding sticky notes)
- **Connections:** 13
- **Triggers:** Schedule · Weekly Metrics

## Integrations (from nodes)
- Airtable
- Code
- Etsy (via HTTP)
- HTTP Request
- IF
- OpenAI (via HTTP)
- Schedule Trigger
- Split In Batches

## AI components (from nodes)
- HTTP · OpenAI Notes → OpenAI Chat

## Inputs / outputs (definition-level)
- **Inputs:** Trigger event + Airtable search/filter rows where present
- **Outputs:** Airtable create/update operations and/or external HTTP calls listed above
- **Needs Review:** Exact Airtable base/table names and field schemas (not copied into portfolio to avoid leaking workspace specifics without privacy review)

## Complexity rationale
Estimated **Advanced** from node count (12), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
