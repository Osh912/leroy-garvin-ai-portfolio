# Developer Documentation — Airtable GH-X MEO Data Layer

## Stack touchpoints
- AI: Stores AI artifacts (prompts, generated URLs) written by n8n
- APIs: Consumed by n8n Airtable nodes (no Airtable native automations observed)
- Airtable: Products, ContentQueue, Settings, Content Engine, GHX Dashboard

## Source of truth
- Public: sanitized markdown only
- Private: JSON exports / ID appendix / Evidence Pack imports where applicable

## Integration notes
Cross-reference Airtable↔n8n: `../../CROSS_REFERENCE_AIRTABLE_N8N.md`

## Security
Never commit credentials. Prefer external secret stores / n8n credentials vault.
