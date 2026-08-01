# GHX-13-Video-Script-Builder

**Portfolio group:** F — Video Pipeline (Script → HeyGen → Poll → QA)  
**Definition source:** `GHX-13-Video-Script-Builder.json` (Desktop GH-X workflows export)  
**Complexity:** Intermediate  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, generate video scripts via OpenAI HTTP for queued rows and save scripts or errors in Airtable.

**Plain English:** Starts on a schedule (`Schedule · Script Build Run`). Airtable `search` via `Airtable · Search Script Queue`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build Script Body`. Transforms/prepares data in Code node `Code · Batch Complete`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Parse Platform Scripts`. Branches with an IF check (`Filter · Script OK`). Airtable `update` via `Airtable · Save Scripts`. Airtable `update` via `Airtable · Log Script Error`.

## Business purpose
On a schedule, generate video scripts via OpenAI HTTP for queued rows and save scripts or errors in Airtable.

## What exists in the definition
- **Nodes:** 10 (excluding sticky notes)
- **Connections:** 11
- **Triggers:** Schedule · Script Build Run

## Integrations (from nodes)
- Airtable
- Code
- HTTP Request
- IF
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
Estimated **Intermediate** from node count (10), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
