# WORKFLOW_EXPORT_GUIDE.md

Manual process only. **Do not** auto-export secrets into the portfolio.

## How to export from n8n (safe)
1. Open n8n → open the workflow
2. Menu → **Download** / **Export** workflow JSON
3. Save outside the git repo first (e.g. Desktop staging folder)
4. Open the JSON in an editor and search for sensitive strings before copying into the portfolio

## Must review / remove before publishing
- Credential IDs paired with usable secrets (never commit raw credential objects)
- Header values containing `Bearer`, `sk-`, API keys
- Webhook URLs with tokens
- Hard-coded emails, phones, addresses
- Private Airtable share links if any
- Pin data / sample execution payloads with PII

## Recommended publish pattern
1. Keep full private export offline
2. Create `*-06-Workflow-Export.sanitized.json` with secrets stripped
3. Store under the workflow’s `evidence/` folder only after privacy gate Pass
4. Document in the workflow Evidence_Checklist that sanitization was completed

## Portfolio policy
- Workflow **definitions were analyzed in place** from Desktop exports
- Sanitized JSON copies are **not** required to claim Functional Build documentation
- Sanitized JSON is required before public GitHub publication of exports
