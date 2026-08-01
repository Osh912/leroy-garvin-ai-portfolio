# GHX-03B-Product-File-Uploader

**Portfolio group:** C — Visual Asset Generation  
**Definition source:** `GHX-03B-Product-File-Uploader.json` (Desktop GH-X workflows export)  
**Complexity:** Advanced  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, build product blueprints/images via OpenAI HTTP and write product file URLs or errors to Airtable.

**Plain English:** Starts on a schedule (`Schedule · Product File Run`). Sets fields (`Set · Load Product Gen Config`). Transforms/prepares data in Code node `Code · Setup Config`. Airtable `search` via `Airtable · Search Needs Product File`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Prepare Product Job`. Transforms/prepares data in Code node `Code · Batch Complete`. Branches with an IF check (`Filter · Job OK`). HTTP request via `HTTP · OpenAI Product Blueprint` (OpenAI Chat). Airtable `update` via `Airtable · Log File Error`. Transforms/prepares data in Code node `Code · Parse Product Blueprint`. Branches with an IF check (`Filter · Blueprint OK`). Routes with a Switch (`Switch · Output Format`). Transforms/prepares data in Code node `Code · Generate Product File · PDF`. HTTP request via `HTTP · OpenAI Product Image` (OpenAI Images). Branches with an IF check (`Filter · Product Binary OK`). Transforms/prepares data in Code node `Code · Image To Binary`. Uses Google Drive (`Google Drive · Upload Product File`).

## Business purpose
On a schedule, build product blueprints/images via OpenAI HTTP and write product file URLs or errors to Airtable.

## What exists in the definition
- **Nodes:** 22 (excluding sticky notes)
- **Connections:** 29
- **Triggers:** Schedule · Product File Run

## Integrations (from nodes)
- Airtable
- Code
- Google Drive
- HTTP Request
- IF
- OpenAI (via HTTP)
- Schedule Trigger
- Set
- Split In Batches
- Switch

## AI components (from nodes)
- HTTP · OpenAI Product Blueprint → OpenAI Chat
- HTTP · OpenAI Product Image → OpenAI Images

## Inputs / outputs (definition-level)
- **Inputs:** Trigger event + Airtable search/filter rows where present
- **Outputs:** Airtable create/update operations and/or external HTTP calls listed above
- **Needs Review:** Exact Airtable base/table names and field schemas (not copied into portfolio to avoid leaking workspace specifics without privacy review)

## Complexity rationale
Estimated **Advanced** from node count (22), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
