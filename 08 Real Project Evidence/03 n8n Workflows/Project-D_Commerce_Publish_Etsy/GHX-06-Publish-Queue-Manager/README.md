# GHX-06-Publish-Queue-Manager

**Portfolio group:** D — Commerce Publish (Etsy)  
**Definition source:** `GHX-06-Publish-Queue-Manager.json` (Desktop GH-X workflows export)  
**Complexity:** Intermediate  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, validate ready-to-publish rows and mark publish-ready or append error logs in Airtable.

**Plain English:** Starts on a schedule (`Schedule · Validation Run`). Airtable `search` via `Airtable · Search Ready To Publish`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Validate Publish Gate`. Transforms/prepares data in Code node `Code · Batch Complete`. Branches with an IF check (`Filter · Complete`). Airtable `update` via `Airtable · Mark Publish Ready`. Airtable `update` via `Airtable · Append Error Log`.

## Business purpose
On a schedule, validate ready-to-publish rows and mark publish-ready or append error logs in Airtable.

## What exists in the definition
- **Nodes:** 8 (excluding sticky notes)
- **Connections:** 9
- **Triggers:** Schedule · Validation Run

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
