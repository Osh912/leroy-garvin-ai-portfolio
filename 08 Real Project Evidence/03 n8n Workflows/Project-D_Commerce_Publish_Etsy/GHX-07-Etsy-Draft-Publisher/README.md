# GHX-07-Etsy-Draft-Publisher

**Portfolio group:** D — Commerce Publish (Etsy)  
**Definition source:** `GHX-07-Etsy-Draft-Publisher.json` (Desktop GH-X workflows export)  
**Complexity:** Advanced  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, create Etsy draft listings and upload images/digital files via HTTP, then save results to Airtable.

**Plain English:** Starts on a schedule (`Schedule · Etsy Draft Run`). Sets fields (`Set · Load Env Config`). Transforms/prepares data in Code node `Code · Setup Config`. Airtable `search` via `Airtable · Search Publish Queue`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build Etsy Payload`. Transforms/prepares data in Code node `Code · Batch Complete`. Branches with an IF check (`Filter · Preflight OK`). HTTP request via `HTTP · Etsy Create Draft`. Airtable `update` via `Airtable · Log Etsy Error`. Transforms/prepares data in Code node `Code · Parse Listing Id`. Branches with an IF check (`Filter · Listing Created`). HTTP request via `HTTP · Download Mockup`. HTTP request via `HTTP · Etsy Upload Image`. HTTP request via `HTTP · Download Digital File`. HTTP request via `HTTP · Etsy Upload Digital File`. Transforms/prepares data in Code node `Code · Build Success Payload`. Airtable `update` via `Airtable · Save Etsy Draft`.

## Business purpose
On a schedule, create Etsy draft listings and upload images/digital files via HTTP, then save results to Airtable.

## What exists in the definition
- **Nodes:** 18 (excluding sticky notes)
- **Connections:** 20
- **Triggers:** Schedule · Etsy Draft Run

## Integrations (from nodes)
- Airtable
- Code
- Etsy (via HTTP)
- HTTP Request
- IF
- Schedule Trigger
- Set
- Split In Batches

## AI components (from nodes)
- None detected in node types/HTTP targets (Needs Review if prompts imply external AI elsewhere)

## Inputs / outputs (definition-level)
- **Inputs:** Trigger event + Airtable search/filter rows where present
- **Outputs:** Airtable create/update operations and/or external HTTP calls listed above
- **Needs Review:** Exact Airtable base/table names and field schemas (not copied into portfolio to avoid leaking workspace specifics without privacy review)

## Complexity rationale
Estimated **Advanced** from node count (18), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
