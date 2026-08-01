# n8n Workflow Automation (Public Capability Overview)

**Who this is for:** Recruiters who want to understand automation skill without downloading workflows  
**Public status:** Functional Build · **Production Ready:** No  
**Updated:** 2026-07-20

## Business problem
Operations work that spans many tools needs reliable orchestration: scheduled runs, queue reads/writes, error handling, and clear handoffs—without relying on fragile manual copy/paste between systems.

## My role
I designed and built the GH-X n8n workflow definitions (23 canonical exports), documented node patterns, and organized them as one system rather than disconnected scripts.

## Solution
Scheduled and queue-driven n8n workflows that search/update Airtable records, call external APIs (where configured), assemble prompts/payloads in Code nodes, and write errors back for retry/QA. Public materials describe capability only.

## Technologies used
n8n · Airtable nodes · Code nodes · HTTP Request patterns · Schedule triggers · Error Trigger (reliability workflow) · service-specific integrations present in definitions (e.g., Drive, Etsy, Metricool, HeyGen—as documented privately)

## Outcome / current status
- Definitions exist and are inventoried privately; public pack explains patterns without importable JSON.
- All exports observed as `active: false` at analysis time; local execution history was empty → **no Production Ready claim**.
- Screenshots of canvases / executions: Evidence Pending.

## Intentionally withheld
Raw workflow JSON (Private Master only) · credentials · webhook URLs · exact proprietary prompts
