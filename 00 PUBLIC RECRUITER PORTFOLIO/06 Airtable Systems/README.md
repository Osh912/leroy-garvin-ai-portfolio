# Airtable Systems (Public)

**Who this is for:** Recruiters reviewing data/ops design for AI automation  
**Public status:** Live schema reviewed (read-only) + design docs · **Production Ready:** No claim  
**Updated:** 2026-07-20

## Business problem
Automation fails when there is no clear place to store status, queues, and errors. Without a shared data layer, workflows cannot hand off work reliably.

## My role
I designed Airtable as the queue/status backbone for GH-X, documented table purpose, and cross-referenced tables to n8n workflows. Live base **GH-X MEO** was reviewed read-only for portfolio documentation.

## Solution
An Airtable base used as the operations data layer: product/content queues, settings, and stage fields that n8n workflows search and update. Public docs describe structure at a safe level (no base/table IDs).

## Technologies used
Airtable · linked with n8n automation · documented views/fields used for stage control

## Outcome / current status
- **Verified in docs:** GH-X MEO — Products, ContentQueue, Settings, Content Engine, GHX Dashboard (tables).
- Native Airtable Automations/Forms/Interfaces hub was empty at review time (Needs Review if that changes).
- Other Home bases (if any) were **not** fully analyzed in this pass → documented only where verified.
- Sanitized screenshots: Evidence Pending.

## See also
[LIVE_BASE_SUMMARY.md](./LIVE_BASE_SUMMARY.md) · sibling files in this folder
