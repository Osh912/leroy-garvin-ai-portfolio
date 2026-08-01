# n8n Workflow — Prompt Engineering

## Purpose
Explain how Prompt Engineering supports AI-assisted steps inside n8n workflow automation concepts.

## Where Prompt Engineering Fits
In prompt-assisted workflow designs, n8n sequences the process while prompts control the quality of AI-assisted outputs before handoff.

```text
n8n Trigger / Prior Stage
  → AI-assisted step (prompt-controlled)
  → Validation / review checkpoint
  → Continue, document, or refine
```

## Prompt Design Pattern for Automation Steps
1. **Task definition** — What the AI-assisted step must produce
2. **Required inputs** — What data must already exist
3. **Expected output format** — What “complete” looks like
4. **Constraints** — Avoid incomplete, off-track, or process-misaligned outputs
5. **Quality checks** — Completeness, clarity, process alignment
6. **Handoff rule** — Pass to next node only after validation

## Testing Prompt Quality Inside Workflows
- Compare AI-assisted output to expected stage behavior
- Determine whether the failure is prompt design vs sequencing vs missing data
- Refine the prompt and/or workflow validation node
- Retest the same path
- Document the change

## Challenges Addressed
- Incomplete AI-assisted outputs reaching the next stage
- Inconsistent results across similar steps
- Difficulty telling prompt problems from automation-logic problems
- Weak review checkpoints before handoff

## ATS / Role Relevance
- Prompt Engineering Support
- AI Quality Assurance
- AI Trainer / evaluation habits
- Workflow Automation Specialist
- AI Operations

## Boundaries
Prompt engineering here supports designed and tested workflow concepts. No production model-deployment claims are made.

**Related:** [Workflow Templates](./Workflow_Templates.md) · [Testing and QA](./Testing_and_QA.md) · [GH-X Prompt Engineering](../04%20GH-X/Prompt_Engineering.md)
