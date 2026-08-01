# Video Pipeline (Script → HeyGen → Poll → QA)

**Portfolio project group:** F
**Workflows in group:** 4
**Source of truth:** n8n workflow definition JSON exports on Desktop (`GH-X/workflows`)
**Execution evidence:** Not found in local n8n DB — do not claim production runs

## Recruiter-friendly summary
Build video scripts, request HeyGen videos, poll status, and QA-gate content readiness in Airtable.

These workflows are documented from **exported definitions**. Export flags show `active: false`. Without execution history screenshots, status is at most **Functional Build** (not Production Ready).

## Workflows
| Workflow | Nodes | Complexity | Status | AI | Key integrations |
|----------|------:|------------|--------|----|------------------|
| [GHX-13-Video-Script-Builder](./GHX-13-Video-Script-Builder/README.md) | 10 | Intermediate | Functional Build | Yes | Airtable, Code, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger |
| [GHX-15-Content-QA](./GHX-15-Content-QA/README.md) | 8 | Intermediate | Functional Build | No / Needs Review | Airtable, Code, IF, Schedule Trigger, Split In Batches |
| [GHX-16-HeyGen-Video-Generator](./GHX-16-HeyGen-Video-Generator/README.md) | 13 | Intermediate | Functional Build | Yes | Airtable, Code, HTTP Request, HeyGen (via HTTP), IF, Schedule Trigger |
| [GHX-17-HeyGen-Status-Poller](./GHX-17-HeyGen-Status-Poller/README.md) | 14 | Intermediate | Functional Build | Yes | Airtable, Code, HTTP Request, HeyGen (via HTTP), IF, Schedule Trigger |

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
