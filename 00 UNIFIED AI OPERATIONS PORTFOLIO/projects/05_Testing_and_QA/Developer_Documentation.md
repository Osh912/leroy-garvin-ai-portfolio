# Developer Documentation — Testing & QA Operations

## Stack touchpoints
- AI: Evaluation of AI outputs / conversational failures
- APIs: Reliability workflows may HTTP alert (destination Needs Review)
- Airtable: qa_status, needs_fix, Error Log fields

## Source of truth
- Public: sanitized markdown only
- Private: JSON exports / ID appendix / Evidence Pack imports where applicable

## Integration notes
Cross-reference Airtable↔n8n: `../../CROSS_REFERENCE_AIRTABLE_N8N.md`

## Security
Never commit credentials. Prefer external secret stores / n8n credentials vault.
