# GHX-05-Social-Asset-Generator

**Portfolio group:** C — Visual Asset Generation  
**Definition source:** `GHX-05-Social-Asset-Generator.json` (Desktop GH-X workflows export)  
**Complexity:** Intermediate  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, process social queue rows with OpenAI Chat via HTTP and update Airtable success/error fields.

**Plain English:** Starts on a schedule (`Schedule · Social Run`). Airtable `search` via `Airtable · Search Social Queue`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build Social Chat Body`. Transforms/prepares data in Code node `Code · Batch Complete`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Parse Social JSON`. Branches with an IF check (`Filter · Parse OK`). Airtable `update` via `Airtable · Update Success`. Airtable `update` via `Airtable · Update Error`.

## Business purpose
On a schedule, process social queue rows with OpenAI Chat via HTTP and update Airtable success/error fields.

## What exists in the definition
- **Nodes:** 10 (excluding sticky notes)
- **Connections:** 11
- **Triggers:** Schedule · Social Run

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
