# GH-X OpenAI Image Generator

**Portfolio group:** C — Visual Asset Generation  
**Definition source:** `GH-X OpenAI Image Generator.json` (Desktop GH-X workflows export)  
**Complexity:** Intermediate  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, find design-ready rows, call OpenAI Images via HTTP, store via Google Drive, and update Airtable.

**Plain English:** Starts on a schedule (`Schedule · Cover Image Run`). Airtable `search` via `Airtable · Search One Ready To Design`. Transforms/prepares data in Code node `Code · Build OpenAI Image Body`. HTTP request via `HTTP · OpenAI Images` (OpenAI Images). Transforms/prepares data in Code node `Code · Response To Binary`. Branches with an IF check (`Filter · Image OK`). Uses Google Drive (`Google Drive · Upload Cover`). Airtable `update` via `Airtable · Log Error`. Transforms/prepares data in Code node `Code · Merge Drive URL`. Airtable `update` via `Airtable · Update By Record Id`.

## Business purpose
On a schedule, find design-ready rows, call OpenAI Images via HTTP, store via Google Drive, and update Airtable.

## What exists in the definition
- **Nodes:** 10 (excluding sticky notes)
- **Connections:** 9
- **Triggers:** Schedule · Cover Image Run

## Integrations (from nodes)
- Airtable
- Code
- Google Drive
- HTTP Request
- IF
- OpenAI (via HTTP)
- Schedule Trigger

## AI components (from nodes)
- HTTP · OpenAI Images → OpenAI Images

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
