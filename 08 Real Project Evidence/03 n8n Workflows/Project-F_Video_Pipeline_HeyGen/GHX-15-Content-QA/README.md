# GHX-15-Content-QA

**Portfolio group:** F — Video Pipeline (Script → HeyGen → Poll → QA)  
**Definition source:** `GHX-15-Content-QA.json` (Desktop GH-X workflows export)  
**Complexity:** Intermediate  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, review QA queue rows and mark video-ready or needs-fix in Airtable.

**Plain English:** Starts on a schedule (`Schedule · Content QA Sweep`). Airtable `search` via `Airtable · Search QA Queue`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Validate Content Fields`. Transforms/prepares data in Code node `Code · Batch Complete`. Branches with an IF check (`Filter · Content Complete`). Airtable `update` via `Airtable · Mark Video Ready`. Airtable `update` via `Airtable · Mark Needs Fix`.

## Business purpose
On a schedule, review QA queue rows and mark video-ready or needs-fix in Airtable.

## What exists in the definition
- **Nodes:** 8 (excluding sticky notes)
- **Connections:** 9
- **Triggers:** Schedule · Content QA Sweep

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
