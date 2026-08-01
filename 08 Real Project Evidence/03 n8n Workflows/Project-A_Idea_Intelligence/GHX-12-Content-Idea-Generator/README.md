# GHX-12-Content-Idea-Generator

**Portfolio group:** A — Idea Intelligence Loop  
**Definition source:** `GHX-12-Content-Idea-Generator.json` (Desktop GH-X workflows export)  
**Complexity:** Intermediate  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, find promotable products, generate content ideas via OpenAI HTTP, and create content rows in Airtable.

**Plain English:** Starts on a schedule (`Schedule · Daily Content Ideas`). Sets fields (`Set · Load Content Niches`). Transforms/prepares data in Code node `Code · Setup Config`. Airtable `search` via `Airtable · Search Promotable Products`. Transforms/prepares data in Code node `Code · Build Daily Ideas Body`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Parse Content Ideas`. Processes records in batches (`Batch · Split Ideas`). Branches with an IF check (`Filter · Idea OK`). Transforms/prepares data in Code node `Code · Run Complete`. Airtable `create` via `Airtable · Create Content Row`. Transforms/prepares data in Code node `Code · Log Skip`.

## Business purpose
On a schedule, find promotable products, generate content ideas via OpenAI HTTP, and create content rows in Airtable.

## What exists in the definition
- **Nodes:** 12 (excluding sticky notes)
- **Connections:** 13
- **Triggers:** Schedule · Daily Content Ideas

## Integrations (from nodes)
- Airtable
- Code
- HTTP Request
- IF
- OpenAI (via HTTP)
- Schedule Trigger
- Set
- Split In Batches

## AI components (from nodes)
- HTTP · OpenAI Chat → OpenAI Chat

## Inputs / outputs (definition-level)
- **Inputs:** Trigger event + Airtable search/filter rows where present
- **Outputs:** Airtable create/update operations and/or external HTTP calls listed above
- **Needs Review:** Exact Airtable base/table names and field schemas (not copied into portfolio to avoid leaking workspace specifics without privacy review)

## Complexity rationale
Estimated **Intermediate** from node count (12), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
