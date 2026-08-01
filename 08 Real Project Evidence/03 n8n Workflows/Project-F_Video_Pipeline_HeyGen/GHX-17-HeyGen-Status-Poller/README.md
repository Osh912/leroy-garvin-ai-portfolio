# GHX-17-HeyGen-Status-Poller

**Portfolio group:** F — Video Pipeline (Script → HeyGen → Poll → QA)  
**Definition source:** `GHX-17-HeyGen-Status-Poller.json` (Desktop GH-X workflows export)  
**Complexity:** Intermediate  
**Status:** Functional Build  
**Production Ready:** No (no execution evidence)  
**Active in export:** `False`

## Recruiter-friendly summary
On a schedule, poll HeyGen status for processing videos and update Airtable ready/failed/error fields.

**Plain English:** Starts on a schedule (`Schedule · Every 10 Minutes`). Airtable `search` via `Airtable · Search Processing Videos`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Prepare Poll Context`. Transforms/prepares data in Code node `Code · Batch Complete`. Branches with an IF check (`Filter · Context OK`). HTTP request via `HTTP · HeyGen Get Status` (HeyGen). Airtable `update` via `Airtable · Log Context Error`. Transforms/prepares data in Code node `Code · Parse HeyGen Status`. Routes with a Switch (`Switch · HeyGen Status`). Airtable `update` via `Airtable · Mark Ready To Schedule`. Transforms/prepares data in Code node `Code · Log Still Processing`. Airtable `update` via `Airtable · Mark Video Failed`. Airtable `update` via `Airtable · Log Poll Error`.

## Business purpose
On a schedule, poll HeyGen status for processing videos and update Airtable ready/failed/error fields.

## What exists in the definition
- **Nodes:** 14 (excluding sticky notes)
- **Connections:** 18
- **Triggers:** Schedule · Every 10 Minutes

## Integrations (from nodes)
- Airtable
- Code
- HTTP Request
- HeyGen (via HTTP)
- IF
- Schedule Trigger
- Split In Batches
- Switch

## AI components (from nodes)
- HTTP · HeyGen Get Status → HeyGen

## Inputs / outputs (definition-level)
- **Inputs:** Trigger event + Airtable search/filter rows where present
- **Outputs:** Airtable create/update operations and/or external HTTP calls listed above
- **Needs Review:** Exact Airtable base/table names and field schemas (not copied into portfolio to avoid leaking workspace specifics without privacy review)

## Complexity rationale
Estimated **Intermediate** from node count (14), branching, batching, and multi-HTTP patterns in the definition.

## Status rationale
Marked **Functional Build** because the export contains a connected node graph with configured integrations, but local execution history was empty and export `active` is `False`. **Not Production Ready.**

## Notes / Needs Review
- Export flag `active: false`.
- No execution evidence in local n8n DB for this export set.

## Links
- [Analysis.md](./Analysis.md)
- [Evidence_Checklist.md](./Evidence_Checklist.md)
- [Privacy_Checklist.md](./Privacy_Checklist.md)
