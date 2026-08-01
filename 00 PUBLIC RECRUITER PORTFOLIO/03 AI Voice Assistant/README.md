# AI Voice Booking Assistant

**Who this is for:** Recruiters reviewing AI Operations / conversational AI / QA work  
**Public status:** Documented Functional Build · **Production Ready:** No  
**Visual evidence:** Evidence Pending (sanitized screenshots not yet in this folder)  
**Updated:** 2026-07-20

## Business problem
Missed or unstructured booking conversations for a local auto detailing business create incomplete details, pricing confusion, and appointments that cannot be confirmed confidently.

## My role
Owner & AI Operations Specialist at Right Outside Auto Detailing LLC. I independently designed conversation logic, prompts, business rules, test cases, and improvement documentation. No employer team was involved.

## Solution
A stage-based booking conversation (greeting → service qualification → vehicle → pricing → confirmation → customer details → appointment → close) with one-question-at-a-time control, confirmation gates, and a structured QA loop (test → classify failure → root cause → fix → retest → document).

## Technologies used (documented scope)
ChatGPT (prompt design and iteration) · workflow design · n8n and Airtable at **concept / process-organization** level · Twilio named only as part of the **voice technology set discussed at documented depth** (no public credentials, numbers, or account IDs).

## Outcome / current status
- Written case study, QA methodology, and improvement notes exist in the portfolio.
- Qualitative improvement of failure patterns (loops, repeated questions, pricing gaps) is documented from testing notes.
- **Not claimed:** call volume, live production metrics, or enterprise deployment.
- **Missing for publication strength:** sanitized screenshots of booking flow / test cases; no public n8n JSON export for this project (none found to include).

## Start here
1. [Business_Problem.md](./Business_Problem.md)
2. [Solution_Overview.md](./Solution_Overview.md)
3. [My_Contribution.md](./My_Contribution.md)
4. [Testing_and_QA.md](./Testing_and_QA.md)
5. [Current_Status.md](./Current_Status.md)
