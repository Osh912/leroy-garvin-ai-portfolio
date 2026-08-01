# Design + Reel Prompt Generator

**Portfolio group:** B — Listing & Prompt Generation  
**Definition source:** `Design + Reel Prompt Generator.json` (Desktop GH-X workflows export)  
**Complexity:** Intermediate  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, search records, build design/reel prompts in Code nodes, and update Airtable.

**Plain English:** Starts on a schedule (`Schedule Trigger`). Airtable `search` via `Search records`. Processes records in batches (`Loop Over Items`). Transforms/prepares data in Code node `Code in JavaScript`. Transforms/prepares data in Code node `Batch complete`. Airtable `update` via `Update record`.

## Business purpose
On a schedule, search records, build design/reel prompts in Code nodes, and update Airtable.

## What exists in the definition
- **Nodes:** 6 (excluding sticky notes)
- **Connections:** 6
- **Triggers:** Schedule Trigger

## Integrations (from nodes)
- Airtable
- Code
- Schedule Trigger
- Split In Batches

## AI components (from nodes)
- None detected in node types/HTTP targets (Needs Review if prompts imply external AI elsewhere)

## Inputs / outputs (definition-level)
- **Inputs:** Trigger event + Airtable search/filter rows where present
- **Outputs:** Airtable create/update operations and/or external HTTP calls listed above
- **Needs Review:** Exact Airtable base/table names and field schemas (not copied into portfolio to avoid leaking workspace specifics without privacy review)

## Complexity rationale
Estimated **Intermediate** from node count (6), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.
- Needs Review: no OpenAI/HeyGen HTTP node visible; prompts appear built in Code nodes only.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
