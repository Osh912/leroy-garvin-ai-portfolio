# PUBLICATION_SANITIZATION_RULES.md

**Date:** 2026-07-20

## Never publish
1. Raw n8n workflow JSON (or backups)
2. `.env` / secret files / credential objects
3. API keys, tokens, OAuth secrets, Authorization headers
4. Webhook URLs, database URLs
5. Airtable base/table IDs, credential IDs
6. Complete proprietary prompts / Code-node prompt bodies
7. Customer names, phones, addresses, emails, financials
8. Private messages, inbox screenshots, browser profile chrome with secrets
9. ServiceFlowAI private source (excluded from public by approval)
10. Private Master Portfolio directory inside a public git repo

## Public may include
- Sanitized architecture Mermaid diagrams (high-level)
- Recruiter case studies with Functional Build / Evidence Pending labels
- Contact info intentionally designated public
- Redacted screenshots after privacy gate Pass
- Copyright and recruiter review notices

## Process
Original file → leave untouched → create sanitized copy or exclude → scan → privacy gate → approve for public folder only.
