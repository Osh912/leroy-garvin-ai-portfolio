# GHX-11-Winning-Idea-Loop

**Portfolio group:** A — Idea Intelligence Loop  
**Definition source:** `GHX-11-Winning-Idea-Loop.json` (Desktop GH-X workflows export)  
**Complexity:** Intermediate  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, read top-performing rows, generate new ideas via OpenAI HTTP, and create idea rows in Airtable.

**Plain English:** Starts on a schedule (`Schedule · Weekly Idea Loop`). Airtable `search` via `Airtable · Search Top Winners`. Transforms/prepares data in Code node `Code · Build Winner Analysis`. Branches with an IF check (`Filter · Has Winners`). HTTP request via `HTTP · OpenAI Ideas` (OpenAI Chat). No-op placeholder (`No Op · No Winners`). Transforms/prepares data in Code node `Code · Parse New Ideas`. Airtable `create` via `Airtable · Create Idea Rows`. Transforms/prepares data in Code node `Code · Run Complete`.

## Business purpose
On a schedule, read top-performing rows, generate new ideas via OpenAI HTTP, and create idea rows in Airtable.

## What exists in the definition
- **Nodes:** 9 (excluding sticky notes)
- **Connections:** 8
- **Triggers:** Schedule · Weekly Idea Loop

## Integrations (from nodes)
- Airtable
- Code
- HTTP Request
- IF
- NoOp
- OpenAI (via HTTP)
- Schedule Trigger

## AI components (from nodes)
- HTTP · OpenAI Ideas → OpenAI Chat

## Inputs / outputs (definition-level)
- **Inputs:** Trigger event + Airtable search/filter rows where present
- **Outputs:** Airtable create/update operations and/or external HTTP calls listed above
- **Needs Review:** Exact Airtable base/table names and field schemas (not copied into portfolio to avoid leaking workspace specifics without privacy review)

## Complexity rationale
Estimated **Intermediate** from node count (9), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
