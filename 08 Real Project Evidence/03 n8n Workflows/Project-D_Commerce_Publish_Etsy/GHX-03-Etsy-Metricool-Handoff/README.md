# GHX-03-Etsy-Metricool-Handoff

**Portfolio group:** D — Commerce Publish (Etsy)  
**Definition source:** `GHX-03-Etsy-Metricool-Handoff.json` (Desktop GH-X workflows export)  
**Complexity:** Beginner  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, search ready rows and prepare/save draft handoff fields in Airtable for publishing prep.

**Plain English:** Starts on a schedule (`Schedule · Publishing Prep`). Airtable `search` via `Airtable · Search Ready Rows`. Transforms/prepares data in Code node `Code · Build Draft JSON`. Airtable `update` via `Airtable · Save Drafts`.

## Business purpose
On a schedule, search ready rows and prepare/save draft handoff fields in Airtable for publishing prep.

## What exists in the definition
- **Nodes:** 4 (excluding sticky notes)
- **Connections:** 3
- **Triggers:** Schedule · Publishing Prep

## Integrations (from nodes)
- Airtable
- Code
- Schedule Trigger

## AI components (from nodes)
- None detected in node types/HTTP targets (Needs Review if prompts imply external AI elsewhere)

## Inputs / outputs (definition-level)
- **Inputs:** Trigger event + Airtable search/filter rows where present
- **Outputs:** Airtable create/update operations and/or external HTTP calls listed above
- **Needs Review:** Exact Airtable base/table names and field schemas (not copied into portfolio to avoid leaking workspace specifics without privacy review)

## Complexity rationale
Estimated **Beginner** from node count (4), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
