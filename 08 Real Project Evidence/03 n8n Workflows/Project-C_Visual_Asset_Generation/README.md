# Visual Asset Generation

**Portfolio project group:** C
**Workflows in group:** 4
**Source of truth:** n8n workflow definition JSON exports on Desktop (`GH-X/workflows`)
**Execution evidence:** Not found in local n8n DB — do not claim production runs

## Recruiter-friendly summary
Generate images, mockups, social assets, and product files; update Airtable (and Google Drive where present).

These workflows are documented from **exported definitions**. Export flags show `active: false`. Without execution history screenshots, status is at most **Functional Build** (not Production Ready).

## Workflows
| Workflow | Nodes | Complexity | Status | AI | Key integrations |
|----------|------:|------------|--------|----|------------------|
| [GH-X OpenAI Image Generator](./GH-X-OpenAI-Image-Generator/README.md) | 10 | Intermediate | Functional Build | Yes | Airtable, Code, Google Drive, HTTP Request, IF, OpenAI (via HTTP) |
| [GHX-03B-Product-File-Uploader](./GHX-03B-Product-File-Uploader/README.md) | 22 | Advanced | Functional Build | Yes | Airtable, Code, Google Drive, HTTP Request, IF, OpenAI (via HTTP) |
| [GHX-04-Mockup-Generator](./GHX-04-Mockup-Generator/README.md) | 15 | Advanced | Functional Build | Yes | Airtable, Code, Google Drive, HTTP Request, IF, OpenAI (via HTTP) |
| [GHX-05-Social-Asset-Generator](./GHX-05-Social-Asset-Generator/README.md) | 10 | Intermediate | Functional Build | Yes | Airtable, Code, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger |

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
