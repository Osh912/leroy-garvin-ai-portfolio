# Idea Intelligence Loop

**Portfolio project group:** A
**Workflows in group:** 3
**Source of truth:** n8n workflow definition JSON exports on Desktop (`GH-X/workflows`)
**Execution evidence:** Not found in local n8n DB — do not claim production runs

## Recruiter-friendly summary
Generate and recycle product/content ideas into Airtable using scheduled runs and OpenAI HTTP calls.

These workflows are documented from **exported definitions**. Export flags show `active: false`. Without execution history screenshots, status is at most **Functional Build** (not Production Ready).

## Workflows
| Workflow | Nodes | Complexity | Status | AI | Key integrations |
|----------|------:|------------|--------|----|------------------|
| [GHX-01-Idea-Intelligence](./GHX-01-Idea-Intelligence/README.md) | 5 | Beginner | Functional Build | Yes | Airtable, Code, HTTP Request, OpenAI (via HTTP), Schedule Trigger |
| [GHX-11-Winning-Idea-Loop](./GHX-11-Winning-Idea-Loop/README.md) | 9 | Intermediate | Functional Build | Yes | Airtable, Code, HTTP Request, IF, NoOp, OpenAI (via HTTP) |
| [GHX-12-Content-Idea-Generator](./GHX-12-Content-Idea-Generator/README.md) | 12 | Intermediate | Functional Build | Yes | Airtable, Code, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger |

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
