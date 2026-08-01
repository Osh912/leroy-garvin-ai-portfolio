# SENSITIVE_DATA_SCAN_REPORT.md

**Date:** 2026-07-20

## Scope
- Scanned: `00 PUBLIC RECRUITER PORTFOLIO/**`
- Private JSON not scanned for display (known high risk; excluded from public by design)

## Structural checks
- Raw JSON files in public tree: **0** (must be 0)
- `.env` files in public tree: **0** (must be 0)

## Keyword findings (secret values NOT displayed)

| File | Line | Pattern | Risk type | Required action | Public-safe |
|------|-----:|---------|-----------|-----------------|-------------|
| `00 PUBLIC RECRUITER PORTFOLIO/PUBLICATION_SANITIZATION_RULES.md` | 7 | secret | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Needs Review |
| `00 PUBLIC RECRUITER PORTFOLIO/PUBLICATION_SANITIZATION_RULES.md` | 8 | token | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Needs Review |
| `00 PUBLIC RECRUITER PORTFOLIO/PUBLICATION_SANITIZATION_RULES.md` | 8 | authorization | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Needs Review |
| `00 PUBLIC RECRUITER PORTFOLIO/PUBLICATION_SANITIZATION_RULES.md` | 7 | credential | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Needs Review |
| `00 PUBLIC RECRUITER PORTFOLIO/PUBLICATION_SANITIZATION_RULES.md` | 9 | webhook | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Needs Review |
| `00 PUBLIC RECRUITER PORTFOLIO/PUBLICATION_SANITIZATION_RULES.md` | 10 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/PUBLICATION_SANITIZATION_RULES.md` | 7 | .env | Mention of sensitive keyword | Review context; OK if educational and no secret value | Needs Review |
| `00 PUBLIC RECRUITER PORTFOLIO/README.md` | 15 | credential | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Needs Review |
| `00 PUBLIC RECRUITER PORTFOLIO/README.md` | 15 | webhook | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Needs Review |
| `00 PUBLIC RECRUITER PORTFOLIO/README.md` | 11 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/TOP_10_PORTFOLIO_PROJECTS.md` | 13 | openai | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/TOP_10_PORTFOLIO_PROJECTS.md` | 10 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/Portfolio_Index.md` | 10 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/10 Legal and Usage Notice/COPYRIGHT_AND_USAGE_NOTICE.md` | 15 | secret | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Needs Review |
| `00 PUBLIC RECRUITER PORTFOLIO/05 n8n Workflow Automation/Solution_Overview.md` | 3 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/05 n8n Workflow Automation/High_Level_Architecture.md` | 8 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/05 n8n Workflow Automation/Tools_and_Integrations.md` | 3 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/04 GH-X Automation System/Project_Summary.md` | 3 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/04 GH-X Automation System/Solution_Overview.md` | 4 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/04 GH-X Automation System/High_Level_Architecture.md` | 8 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/04 GH-X Automation System/Tools_and_Integrations.md` | 12 | token | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Needs Review |
| `00 PUBLIC RECRUITER PORTFOLIO/04 GH-X Automation System/Tools_and_Integrations.md` | 6 | openai | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/04 GH-X Automation System/Tools_and_Integrations.md` | 5 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/04 GH-X Automation System/README.md` | 19 | token | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Needs Review |
| `00 PUBLIC RECRUITER PORTFOLIO/04 GH-X Automation System/README.md` | 19 | credential | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Needs Review |
| `00 PUBLIC RECRUITER PORTFOLIO/04 GH-X Automation System/README.md` | 19 | webhook | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Needs Review |
| `00 PUBLIC RECRUITER PORTFOLIO/04 GH-X Automation System/README.md` | 8 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/04 GH-X Automation System/Skills_Demonstrated.md` | 6 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/03 AI Voice Assistant/Tools_and_Integrations.md` | 5 | secret | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Needs Review |
| `00 PUBLIC RECRUITER PORTFOLIO/03 AI Voice Assistant/Tools_and_Integrations.md` | 5 | credential | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Needs Review |
| `00 PUBLIC RECRUITER PORTFOLIO/03 AI Voice Assistant/Tools_and_Integrations.md` | 3 | twilio | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/03 AI Voice Assistant/Tools_and_Integrations.md` | 3 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/01 Resume/FINAL_MASTER_RESUME.md` | 53 | twilio | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/01 Resume/FINAL_MASTER_RESUME.md` | 16 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/06 Airtable Systems/Workflow_Overview.md` | 3 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/06 Airtable Systems/My_Contribution.md` | 3 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/06 Airtable Systems/Tools_and_Integrations.md` | 3 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/06 Airtable Systems/README.md` | 1 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/02 About and Contact/README.md` | 12 | airtable | Tool/process mention without secret value detected | Keep if no secret; avoid IDs | Yes |

## Private JSON risk summary (no values)
- Canonical private exports: **23** files under Original JSON Exports
- Typical risks: Authorization headers, Airtable IDs, API endpoints, proprietary prompts
- **Required action:** Never publish; keep private only

## Verdict
Public tree contains documentation keywords (OpenAI/Airtable/etc.) expected in recruiter materials.
No raw JSON or .env detected in public tree at scan time.
Still **not Ready to Publish** until screenshots pass privacy gate and final audit is green.
