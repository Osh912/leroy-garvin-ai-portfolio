# GH-X Master Automation (Local n8n Stub)

**Source:** Local n8n database (`~/.n8n`) — not a Desktop GH-X export  
**Status:** Prototype  
**Complexity:** Beginner  
**Execution evidence:** 0 executions in local DB  
**Production Ready:** No

## Recruiter summary
A minimal local workflow with a Manual Trigger connected to an Airtable Search node. Airtable base/table selectors were empty at analysis time. This is documented for completeness and is **not** presented as a finished GH-X pipeline workflow.

## Nodes
1. When clicking ‘Execute workflow’ (`manualTrigger`)
2. Search records (`airtable` / operation: search)

## Connection
Manual Trigger → Search records

## Integrations
Manual Trigger, Airtable

## AI components
None

## Needs Review
- Whether this stub was intended as a starter for a larger master orchestrator
- Whether base/table were intentionally unset
