# MANUAL_EVIDENCE_CAPTURE_GUIDE.md

Capture screenshots manually. Do not invent images.

## n8n workflows (required for recruiter-ready evidence)

### For each selected workflow
| Step | Application | What to open | Must be visible | Must NOT be visible | Zoom | Filename pattern | Destination | Required? |
|------|-------------|--------------|-----------------|---------------------|------|------------------|-------------|-----------|
| 1 | n8n | Workflow canvas | Full node graph | Credential values, PII | Fit to screen | `*-01-Workflow-Canvas.png` | Matching workflow folder / `evidence/` | Required |
| 2 | n8n | Same workflow | Main path readable | Secrets | 125–150% | `*-02-Key-Nodes.png` | same | Required |
| 3 | n8n | Key node settings | Operation + non-secret options | Tokens/keys | 150% | `*-03-Node-Configuration.png` | same | Required |
| 4 | n8n | Executions tab | History list or empty-state | Payload PII | 100% | `*-04-Execution-History.png` | same | Required (even if empty) |
| 5 | n8n / target app | Output sample | Safe sample only | Customer data | 100% | `*-05-Output.png` | same | Optional |
| 6 | Editor | Sanitized JSON | Structure only | Secrets | n/a | `*-06-Workflow-Export.json` | same | Optional until GitHub |

### Priority capture order (suggested)
1. GHX-03B-Product-File-Uploader (Advanced, multi-AI HTTP)
2. GHX-07-Etsy-Draft-Publisher
3. GHX-04-Mockup-Generator
4. GHX-16 + GHX-17 (HeyGen pair)
5. GHX-01-Idea-Intelligence
6. GHX-00-Error-Alerts

## AI Voice Assistant
| Filename | App | Open | Visible | Hide | Required? |
|----------|-----|------|---------|------|-----------|
| VA-01-Booking-Flow.png | Docs / tool UI | Booking stage map | Stages | Customer PII | Required |
| VA-02-System-Prompt.png | Prompt doc/tool | System prompt | Structure | Secrets | Required |
| VA-03-Business-Rules.png | Docs | Rules | Rules list | PII | Required |
| VA-04-Test-Cases.png | QA notes | Test table | Cases | Raw customer data | Required |
| VA-05-Root-Cause-Analysis.png | QA notes | RCA sample | Cause/fix | PII | Required |
| VA-06-System-Evidence.png | Tool UI | Safe config | Non-secret config | Twilio secrets | Optional |

## Airtable
| Filename | App | Open | Visible | Hide | Required? |
|----------|-----|------|---------|------|-----------|
| AT-01-Base-Overview.png | Airtable | Base home | Table names | Record PII | Required |
| AT-02-Table-Structure.png | Airtable | Grid view | Fields | Private values | Required |
| AT-03-Fields.png | Airtable | Field config | Types | Secrets | Required |
| AT-04-Relationships.png | Airtable | Links | Relationship | PII | Optional |
| AT-05-Automation-Connection.png | Airtable/n8n | Connection proof | Non-secret | Tokens | Optional |

## Cursor Development
| Filename | App | Open | Visible | Hide | Required? |
|----------|-----|------|---------|------|-----------|
| CU-01-Portfolio-Folders.png | Cursor | Explorer | Folder tree | Secrets/.env | Optional |
| CU-02-Doc-Refinement.png | Cursor | Sample doc edit | Truthful revision | Irrelevant personal files | Optional |

Always run [EVIDENCE_PRIVACY_GATE.md](./EVIDENCE_PRIVACY_GATE.md) before filing images.
