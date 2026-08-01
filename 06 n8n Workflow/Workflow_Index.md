# n8n Workflow Index

## Recruiter Summary
This folder documents no-code Workflow Automation concepts designed and tested in n8n to support AI Operations work across the AI Voice Booking Assistant and GH-X projects. The focus is stage sequencing, handoffs, review checkpoints, prompt-assisted step review, failure logging, process documentation, and continuous improvement. These workflows are documented as designed and tested concepts—not claimed enterprise production deployments.

**Scope note:** No user counts, revenue, uptime, or production-scale metrics are claimed. Credentials and secrets are never stored in portfolio files.

## Related Evidence
- [Workflow Templates](./Workflow_Templates.md)
- [Testing and QA](./Testing_and_QA.md)
- [Prompt Engineering](./Prompt_Engineering.md)
- [Troubleshooting](./Troubleshooting.md)
- [AI Voice Booking Assistant](../03%20AI%20Voice%20Assistant/Project_Overview.md)
- [GH-X](../04%20GH-X/Project_Overview.md)
- [n8n Screenshot Evidence Checklist](../08%20Screenshots/n8n_Workflow.md)

---

## Purpose
Index of real n8n workflow ideas designed and tested as part of AI-assisted business automation work for Right Outside Auto Detailing LLC operations support and GH-X digital product workflow concepts.

## Business Problem
Manual, repetitive process steps and unclear handoffs reduce operational consistency. Without clear sequencing, review checkpoints, and documentation, AI-assisted and manual process steps become harder to test, troubleshoot, and improve.

## My Responsibilities
- Designed workflow logic and automation ideas in n8n
- Connected process steps into sequenced workflow concepts
- Built review checkpoint and failure-logging patterns
- Coordinated prompt-assisted steps with automation sequencing where applicable
- Tested automation ideas for weak transitions and unclear logic
- Documented workflow behavior, issues, and improvements

## Workflow Inventory
| Workflow Name | Purpose | Status | ATS Focus | Related Files |
|---------------|---------|--------|-----------|---------------|
| Booking Process Sequencing Concept | Support stage-based voice booking workflow organization | Designed & tested as concept *(n8n JSON not found)* | Workflow Automation, AI Operations | [AI Voice Assistant Workflow](../03%20AI%20Voice%20Assistant/Workflow_Design.md) |
| GH-X digital product workflows (23 exports) | Idea → assets → publish → video → QA → metrics | **Functional Build** from definitions; **not Production Ready** (no execution evidence) | Workflow Automation, AI Operations | [Real n8n Evidence](../08%20Real%20Project%20Evidence/03%20n8n%20Workflows/README.md) |

**Authoritative inventory:** [n8n_Workflow_Inventory.md](../08%20Real%20Project%20Evidence/03%20n8n%20Workflows/n8n_Workflow_Inventory.md)

## Categories
### Workflow Automation
- Stage sequencing
- Process handoffs
- Review checkpoint triggers
- Status update concepts

### AI Operations / Integrations (Concept Level)
- Airtable record/status planning concepts
- AI-assisted step documentation
- Booking workflow support concepts

### AI Quality Assurance / Content Ops Support
- Process documentation support
- Failure review and refinement loops
- Retest reminders after issue classification

## High-Level Automation Logic
Each n8n workflow concept follows this pattern:

1. **Trigger** — What starts the workflow or stage
2. **Validate** — Confirm required inputs or prior-stage readiness
3. **Action** — Execute the next process or AI-assisted step
4. **Review Checkpoint** — Human or rules-based quality check when needed
5. **Status / Documentation Update** — Record outcome for traceability
6. **Handoff or Refine** — Continue to next stage or return for correction

## Technologies Used (Scope Labels)
| Technology | How it was used |
|------------|-----------------|
| n8n | Primary no-code workflow automation design and testing environment |
| Airtable | Related status/record planning concepts for process tracking |
| ChatGPT / Claude | Prompt design and refinement for AI-assisted workflow steps |
| Process documentation | Issue notes, workflow descriptions, continuous improvement records |

## Transferable Skills (Role Mapping)
| Skill | Relevant roles |
|-------|----------------|
| Stage sequencing and handoffs | Workflow Automation Specialist, AI Operations |
| Review checkpoints and failure logging | AI Quality Assurance, AI Support Engineer |
| Prompt-assisted step design | Prompt Engineering Support, AI Trainer |
| Structured troubleshooting | AI Support Engineer, AI Operations |
| Process documentation | AI Operations, Workflow Automation |

## Notes
- Document workflows as concepts unless separately verified as production deployments
- Never store API keys or credentials in portfolio files
- Naming convention: `project_stage_action_v1`
- Capture sanitized screenshots for employer evidence pack
