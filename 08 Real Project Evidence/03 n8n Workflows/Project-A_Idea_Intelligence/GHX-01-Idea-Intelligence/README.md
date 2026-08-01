# GHX-01-Idea-Intelligence

**Portfolio group:** A — Idea Intelligence Loop  
**Definition source:** `GHX-01-Idea-Intelligence.json` (Desktop GH-X workflows export)  
**Complexity:** Beginner  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, generate product ideas (OpenAI HTTP) and create Airtable product records.

**Plain English:** Starts on a schedule (`Schedule · Weekly Ideas`). Transforms/prepares data in Code node `Code · Build OpenAI Body`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Parse Ideas`. Airtable `create` via `Airtable · Create Product`.

## Business purpose
On a schedule, generate product ideas (OpenAI HTTP) and create Airtable product records.

## What exists in the definition
- **Nodes:** 5 (excluding sticky notes)
- **Connections:** 4
- **Triggers:** Schedule · Weekly Ideas

## Integrations (from nodes)
- Airtable
- Code
- HTTP Request
- OpenAI (via HTTP)
- Schedule Trigger

## AI components (from nodes)
- HTTP · OpenAI Chat → OpenAI Chat

## Inputs / outputs (definition-level)
- **Inputs:** Trigger event + Airtable search/filter rows where present
- **Outputs:** Airtable create/update operations and/or external HTTP calls listed above
- **Needs Review:** Exact Airtable base/table names and field schemas (not copied into portfolio to avoid leaking workspace specifics without privacy review)

## Complexity rationale
Estimated **Beginner** from node count (5), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
