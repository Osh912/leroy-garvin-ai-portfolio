# Listing & Prompt Generation

**Portfolio project group:** B
**Workflows in group:** 2
**Source of truth:** n8n workflow definition JSON exports on Desktop (`GH-X/workflows`)
**Execution evidence:** Not found in local n8n DB — do not claim production runs

## Recruiter-friendly summary
Turn idea/product records into listing copy or design/reel prompts and write results back to Airtable.

These workflows are documented from **exported definitions**. Export flags show `active: false`. Without execution history screenshots, status is at most **Functional Build** (not Production Ready).

## Workflows
| Workflow | Nodes | Complexity | Status | AI | Key integrations |
|----------|------:|------------|--------|----|------------------|
| [Design + Reel Prompt Generator](./Design-Reel-Prompt-Generator/README.md) | 6 | Intermediate | Functional Build | No / Needs Review | Airtable, Code, Schedule Trigger, Split In Batches |
| [GHX-Generate-Product-Listing](./GHX-Generate-Product-Listing/README.md) | 10 | Intermediate | Functional Build | Yes | Airtable, Code, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger |

## Shared pattern (from definitions)
1. Schedule (or error) trigger
2. Airtable search / read queue rows
3. Optional batching + Code transforms
4. Optional HTTP to OpenAI / HeyGen / Metricool / Etsy
5. Airtable update/create success or error fields

## Related written portfolio docs
- [06 n8n Workflow/](../../../06%20n8n%20Workflow/)
- [04 GH-X/](../../../04%20GH-X/)
- [07 Airtable/](../../../07%20Airtable/)
