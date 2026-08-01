# Developer Documentation — GH-X Content & Product Automation System

## Stack touchpoints
- AI: OpenAI Chat/Images via HTTP; HeyGen video APIs
- APIs: OpenAI, Etsy, Metricool, HeyGen, Google Drive, Airtable
- Airtable: GH-X MEO: Products, ContentQueue, Settings, Content Engine, GHX Dashboard

## Source of truth
- Public: sanitized markdown only
- Private: JSON exports / ID appendix / Evidence Pack imports where applicable

## Integration notes
Cross-reference Airtable↔n8n: `../../CROSS_REFERENCE_AIRTABLE_N8N.md`

## Security
Never commit credentials. Prefer external secret stores / n8n credentials vault.
