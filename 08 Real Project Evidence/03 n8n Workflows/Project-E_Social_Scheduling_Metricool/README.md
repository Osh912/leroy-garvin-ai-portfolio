# Social Scheduling (Metricool)

**Portfolio project group:** E
**Workflows in group:** 3
**Source of truth:** n8n workflow definition JSON exports on Desktop (`GH-X/workflows`)
**Execution evidence:** Not found in local n8n DB — do not claim production runs

## Recruiter-friendly summary
Build social post packs, schedule via Metricool HTTP where configured, and maintain ready-to-post queues in Airtable.

These workflows are documented from **exported definitions**. Export flags show `active: false`. Without execution history screenshots, status is at most **Functional Build** (not Production Ready).

## Workflows
| Workflow | Nodes | Complexity | Status | AI | Key integrations |
|----------|------:|------------|--------|----|------------------|
| [GHX-08-Metricool-Scheduler](./GHX-08-Metricool-Scheduler/README.md) | 16 | Advanced | Functional Build | Yes | Airtable, Code, HTTP Request, IF, Metricool (via HTTP), OpenAI (via HTTP) |
| [GHX-09-Ready-To-Post-Queue](./GHX-09-Ready-To-Post-Queue/README.md) | 11 | Intermediate | Functional Build | No / Needs Review | Airtable, Code, IF, Schedule Trigger, Split In Batches |
| [GHX-14-Metricool-Content-Scheduler](./GHX-14-Metricool-Content-Scheduler/README.md) | 16 | Advanced | Functional Build | Yes | Airtable, Code, HTTP Request, IF, Metricool (via HTTP), OpenAI (via HTTP) |

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
