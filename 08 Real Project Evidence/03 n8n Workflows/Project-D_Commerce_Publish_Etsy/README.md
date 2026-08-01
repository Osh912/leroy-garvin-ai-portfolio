# Commerce Publish (Etsy)

**Portfolio project group:** D
**Workflows in group:** 3
**Source of truth:** n8n workflow definition JSON exports on Desktop (`GH-X/workflows`)
**Execution evidence:** Not found in local n8n DB — do not claim production runs

## Recruiter-friendly summary
Validate publish-ready rows, prepare handoffs, and create Etsy draft listings with asset uploads via HTTP.

These workflows are documented from **exported definitions**. Export flags show `active: false`. Without execution history screenshots, status is at most **Functional Build** (not Production Ready).

## Workflows
| Workflow | Nodes | Complexity | Status | AI | Key integrations |
|----------|------:|------------|--------|----|------------------|
| [GHX-03-Etsy-Metricool-Handoff](./GHX-03-Etsy-Metricool-Handoff/README.md) | 4 | Beginner | Functional Build | No / Needs Review | Airtable, Code, Schedule Trigger |
| [GHX-06-Publish-Queue-Manager](./GHX-06-Publish-Queue-Manager/README.md) | 8 | Intermediate | Functional Build | No / Needs Review | Airtable, Code, IF, Schedule Trigger, Split In Batches |
| [GHX-07-Etsy-Draft-Publisher](./GHX-07-Etsy-Draft-Publisher/README.md) | 18 | Advanced | Functional Build | No / Needs Review | Airtable, Code, Etsy (via HTTP), HTTP Request, IF, Schedule Trigger |

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
