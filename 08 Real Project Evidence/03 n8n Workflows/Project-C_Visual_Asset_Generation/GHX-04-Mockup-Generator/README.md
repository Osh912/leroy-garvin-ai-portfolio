# GHX-04-Mockup-Generator

**Portfolio group:** C — Visual Asset Generation  
**Definition source:** `GHX-04-Mockup-Generator.json` (Desktop GH-X workflows export)  
**Complexity:** Advanced  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, process mockup queue rows with OpenAI Chat + Images, store assets (Google Drive), and update Airtable.

**Plain English:** Starts on a schedule (`Schedule · Mockup Run`). Airtable `search` via `Airtable · Search Mockup Queue`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build Mockup Chat Body`. Transforms/prepares data in Code node `Code · Batch Complete`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Parse Mockup Prompt`. Branches with an IF check (`Filter · Prompt OK`). HTTP request via `HTTP · OpenAI Images` (OpenAI Images). Airtable `update` via `Airtable · Update Error`. Transforms/prepares data in Code node `Code · Image To Binary`. Branches with an IF check (`Filter · Image OK`). Uses Google Drive (`Google Drive · Upload Mockup`). Transforms/prepares data in Code node `Code · Merge Drive Link`. Airtable `update` via `Airtable · Update Success`.

## Business purpose
On a schedule, process mockup queue rows with OpenAI Chat + Images, store assets (Google Drive), and update Airtable.

## What exists in the definition
- **Nodes:** 15 (excluding sticky notes)
- **Connections:** 17
- **Triggers:** Schedule · Mockup Run

## Integrations (from nodes)
- Airtable
- Code
- Google Drive
- HTTP Request
- IF
- OpenAI (via HTTP)
- Schedule Trigger
- Split In Batches

## AI components (from nodes)
- HTTP · OpenAI Chat → OpenAI Chat
- HTTP · OpenAI Images → OpenAI Images

## Inputs / outputs (definition-level)
- **Inputs:** Trigger event + Airtable search/filter rows where present
- **Outputs:** Airtable create/update operations and/or external HTTP calls listed above
- **Needs Review:** Exact Airtable base/table names and field schemas (not copied into portfolio to avoid leaking workspace specifics without privacy review)

## Complexity rationale
Estimated **Advanced** from node count (15), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
