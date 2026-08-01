# Developer Documentation — n8n Workflow Automation Capability

## Stack touchpoints
- AI: HTTP OpenAI/HeyGen in multiple workflows
- APIs: Airtable, OpenAI, Drive, Etsy, Metricool, HeyGen
- Airtable: Primary system of record for queues

## Source of truth
- Public: sanitized markdown only
- Private: JSON exports / ID appendix / Evidence Pack imports where applicable

## Integration notes
Cross-reference Airtable↔n8n: `../../CROSS_REFERENCE_AIRTABLE_N8N.md`

## Security
Never commit credentials. Prefer external secret stores / n8n credentials vault.
