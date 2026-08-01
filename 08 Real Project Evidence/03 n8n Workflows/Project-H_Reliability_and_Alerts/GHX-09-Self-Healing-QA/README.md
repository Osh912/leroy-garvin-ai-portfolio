# GHX-09-Self-Healing-QA

**Portfolio group:** H — Reliability & Alerts  
**Definition source:** `GHX-09-Self-Healing-QA.json` (Desktop GH-X workflows export)  
**Complexity:** Intermediate  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, find failed rows and requeue for retry or flag for manual review in Airtable.

**Plain English:** Starts on a schedule (`Schedule · QA Sweep`). Airtable `search` via `Airtable · Search Failed Rows`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Classify Failure`. Transforms/prepares data in Code node `Code · Batch Complete`. Branches with an IF check (`Filter · Can Auto Retry`). Airtable `update` via `Airtable · Requeue For Retry`. Airtable `update` via `Airtable · Flag Manual Review`. Branches with an IF check (`Filter · Webhook Set`). HTTP request via `HTTP · Admin Alert`. No-op placeholder (`No Op · Skip Alert`).

## Business purpose
On a schedule, find failed rows and requeue for retry or flag for manual review in Airtable.

## What exists in the definition
- **Nodes:** 11 (excluding sticky notes)
- **Connections:** 13
- **Triggers:** Schedule · QA Sweep

## Integrations (from nodes)
- Airtable
- Code
- HTTP Request
- IF
- NoOp
- Schedule Trigger
- Split In Batches

## AI components (from nodes)
- None detected in node types/HTTP targets (Needs Review if prompts imply external AI elsewhere)

## Inputs / outputs (definition-level)
- **Inputs:** Trigger event + Airtable search/filter rows where present
- **Outputs:** Airtable create/update operations and/or external HTTP calls listed above
- **Needs Review:** Exact Airtable base/table names and field schemas (not copied into portfolio to avoid leaking workspace specifics without privacy review)

## Complexity rationale
Estimated **Intermediate** from node count (11), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
