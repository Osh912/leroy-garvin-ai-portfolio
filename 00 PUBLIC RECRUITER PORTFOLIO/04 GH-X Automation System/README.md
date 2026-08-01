# GH-X Automation System

**Who this is for:** Recruiters reviewing AI Operations / workflow automation  
**Public status:** Functional Build (definition-based) · **Production Ready:** No  
**Execution evidence:** Evidence Pending  
**Updated:** 2026-07-20

## Business problem
Creating and publishing digital product assets requires many handoffs (ideas → copy → images → listings → social/video → measurement). Manual handoffs are easy to skip, hard to QA, and difficult to improve systematically.

## My role
I independently designed and configured the GH-X automation workflow definitions and queue-oriented process flow, including prompt/payload assembly patterns and multi-service orchestration across the pipeline stages.

## Solution
A multi-stage operations automation system built around Airtable queues and n8n scheduled workflows. Stages cover ideation, listing/prompt generation, visual assets, commerce draft publishing, social scheduling, video generation/polling, performance feedback, and reliability controls.

## Technologies used (verified from definitions + live schema review)
n8n · Airtable (GH-X MEO tables as queue/status layer) · AI image generation APIs (as configured in workflows) · Google Drive · Etsy/Metricool/HeyGen HTTP patterns where present in definitions · ChatGPT/Claude for design and documentation support

## Outcome / current status
- **Verified:** 23 canonical n8n workflow definitions (Desktop; copies in Private Master only) · live Airtable GH-X MEO schema documented (5 tables) · public sanitized case-study narrative
- **Not verified / not claimed:** production-ready status, execution volume, revenue, or customer counts
- **Evidence Pending for GitHub strength:** workflow canvas screenshots, sanitized Airtable screenshots, honest execution-history capture (empty state is acceptable if accurate)

## What is intentionally withheld
Raw n8n JSON · complete proprietary prompts · credentials/tokens/webhooks · base/table IDs · customer-identifying data

## Start here
1. [Business_Problem.md](./Business_Problem.md)
2. [Solution_Overview.md](./Solution_Overview.md)
3. [Workflow_Overview.md](./Workflow_Overview.md)
4. [My_Contribution.md](./My_Contribution.md)
5. [Current_Status.md](./Current_Status.md)
