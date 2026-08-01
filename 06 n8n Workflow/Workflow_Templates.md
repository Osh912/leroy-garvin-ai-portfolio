# n8n Workflow Templates

## Purpose
Reusable no-code Workflow Automation patterns from real GH-X and AI Voice Assistant workflow design work. These templates describe workflows actually designed or tested as concepts.

## Recruiter / Hiring Manager Note
Each template is written so a recruiter can understand the business purpose quickly, while a technical reviewer can see trigger → nodes → validation → handoff logic.

---

## Template 1 — Stage Sequencing Workflow
### Business Use Case
Move a process through defined stages with clear handoff conditions. Used for booking-process support and digital product workflow concepts.

### Automation Logic
```text
Trigger → Stage Validation → Next-Step Action → Status Update → Review Checkpoint → Handoff
```

### Trigger
New process record or stage-ready status

### Key Nodes / Steps
1. Trigger event
2. Validate required inputs / prior stage completion
3. Execute next-step action
4. Update stage status
5. Optional review checkpoint
6. Hand off to next stage

### Outputs
- Updated stage status
- Documented handoff readiness

### Testing Focus
- Correct stage order
- Missing-input handling
- Clear handoff conditions

### ATS Keywords Demonstrated
Workflow Automation · AI Operations · Process Documentation · Continuous Improvement

### Notes
Used for booking and digital product workflow concepts.

---

## Template 2 — Prompt-Assisted Review Handoff
### Business Use Case
Send an AI-assisted step output to a review/documentation step before continuing. Supports Prompt Engineering and AI Quality Assurance habits inside automation design.

### Automation Logic
```text
AI Step Complete → Capture Output → Validation Check → Review Branch
  → Pass: Document + Continue
  → Fail: Refine Prompt / Logic + Retest Path
```

### Trigger
AI-assisted step completion

### Key Nodes / Steps
1. Input / output capture
2. Output validation check (completeness, clarity, process alignment)
3. Review branch
4. Document result
5. Continue or refine

### Prompt Engineering Tie-In
- Define the AI-assisted task clearly
- Specify expected output format
- Add constraints to reduce incomplete or off-track responses
- Refine prompts after failed validation

### Outputs
- Reviewed output
- Issue note
- Refinement trigger when quality checks fail

### Testing Focus
- Incomplete AI outputs
- Process-misaligned responses
- Whether review checkpoints catch weak results before handoff

### ATS Keywords Demonstrated
Prompt Engineering · AI Quality Assurance · Conversational / AI-assisted step review · Workflow Automation

### Notes
Supports AI QA and Prompt Engineering Support workflows.

---

## Template 3 — Failure Logging Pattern
### Business Use Case
Record an observed workflow failure, classify the issue, and queue it for retest. Aligns with AI Operations troubleshooting and continuous improvement.

### Automation Logic
```text
Failure Detected → Capture Details → Classify Cause → Update Documentation → Retest Reminder
```

### Trigger
Failed scenario test or weak automation transition

### Key Nodes / Steps
1. Failure capture
2. Classification (node config, sequencing, missing data, prompt issue, documentation gap)
3. Documentation update
4. Retest reminder

### Root Cause Categories Used
- Node configuration
- Sequencing logic
- Missing required data
- Prompt instructions (if AI-assisted)
- Incomplete process rules

### Outputs
- Structured issue record
- Clear retest path

### Testing Focus
- Whether failures are classified consistently
- Whether documentation supports later retesting
- Whether the same issue can be reproduced and rechecked

### ATS Keywords Demonstrated
Root Cause Analysis · AI Quality Assurance · Process Documentation · Continuous Improvement · AI Support troubleshooting

### Notes
Aligns with AI Operations and QA documentation practices.

---

## Template Comparison (Quick Scan)

| Template | Primary Goal | Best Role Fit |
|----------|--------------|---------------|
| Stage Sequencing | Reliable process order | Workflow Automation, AI Operations |
| Prompt-Assisted Review | Quality-controlled AI steps | Prompt Engineering, AI QA |
| Failure Logging | Structured troubleshooting | AI Support, AI Operations, AI QA |

## Reuse Guidelines
- Sanitize all screenshots and exports before sharing
- Document expected behavior before building additional nodes
- Keep secrets out of portfolio files
- Label concept workflows honestly
- Prefer one clear purpose per workflow template

**Related:** [Workflow Index](./Workflow_Index.md) · [Testing and QA](./Testing_and_QA.md) · [Prompt Engineering](./Prompt_Engineering.md) · [Troubleshooting](./Troubleshooting.md)
