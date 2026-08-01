# Reliability & Alerts

**Portfolio project group:** H
**Workflows in group:** 2
**Source of truth:** n8n workflow definition JSON exports on Desktop (`GH-X/workflows`)
**Execution evidence:** Not found in local n8n DB — do not claim production runs

## Recruiter-friendly summary
Catch workflow errors and requeue or flag failed Airtable rows for retry or manual review.

These workflows are documented from **exported definitions**. Export flags show `active: false`. Without execution history screenshots, status is at most **Functional Build** (not Production Ready).

## Workflows
| Workflow | Nodes | Complexity | Status | AI | Key integrations |
|----------|------:|------------|--------|----|------------------|
| [GHX-00-Error-Alerts](./GHX-00-Error-Alerts/README.md) | 5 | Beginner | Functional Build | No / Needs Review | Code, Error Trigger, HTTP Request, IF, NoOp |
| [GHX-09-Self-Healing-QA](./GHX-09-Self-Healing-QA/README.md) | 11 | Intermediate | Functional Build | No / Needs Review | Airtable, Code, HTTP Request, IF, NoOp, Schedule Trigger |

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
