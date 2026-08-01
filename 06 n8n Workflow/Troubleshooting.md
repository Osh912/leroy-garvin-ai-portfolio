# n8n Workflow — Troubleshooting

## Purpose
Document the troubleshooting and root cause analysis process used when n8n workflow automation concepts failed testing or behaved unclearly.

## Troubleshooting Process
1. Reproduce the issue with the same sample inputs
2. Identify where the workflow broke (trigger, validation, action, review, handoff)
3. Classify the likely cause
4. Apply a targeted fix
5. Retest the same scenario
6. Update documentation

## Root Cause Categories
| Cause Bucket | Examples | Typical Fix Direction |
|--------------|----------|------------------------|
| Node configuration | Wrong setup or unclear node purpose | Clarify node role and required settings |
| Sequencing logic | Steps out of order or weak handoffs | Tighten stage order and validation |
| Missing required data | Workflow continues without needed inputs | Strengthen input checks |
| Prompt instructions | AI-assisted output incomplete or off-track | Refine prompt constraints and expected format |
| Incomplete process rules | Unclear when to continue vs review | Add review checkpoints and handoff rules |
| Documentation gaps | Hard to understand or retest later | Improve process notes and issue records |

## Sample Troubleshooting Table

| Symptom | Likely Cause | Troubleshooting Action |
|---------|--------------|------------------------|
| Workflow skips a needed check | Sequencing / missing validation | Add stage validation before next-step action |
| AI output is incomplete but process continues | Prompt issue + weak review checkpoint | Strengthen validation and refine prompt |
| Status is unclear after a run | Incomplete process rules / documentation | Improve status update and documentation step |
| Same failure repeats after a change | Misclassified root cause | Re-run cause classification; separate prompt vs sequencing |
| Hard to retest later | Documentation gap | Use failure-logging template and retest reminder |

## AI Support / AI Operations Relevance
This troubleshooting approach demonstrates:
- Structured problem solving
- Root cause analysis
- Process documentation
- Continuous improvement
- Clear communication of technical issues

## Boundaries
These are troubleshooting methods for designed and tested workflow concepts. No production incident volumes or SLA metrics are claimed.

**Related:** [Testing and QA](./Testing_and_QA.md) · [Workflow Templates](./Workflow_Templates.md) · [Workflow Index](./Workflow_Index.md)
