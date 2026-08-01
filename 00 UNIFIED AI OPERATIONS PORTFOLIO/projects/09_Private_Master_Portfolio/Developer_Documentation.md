# Developer Documentation — Private Master Portfolio (Confidential Vault)

## Stack touchpoints
- AI: Contains private workflow defs with AI HTTP configs
- APIs: Private JSON may embed auth patterns — never publish
- Airtable: Private live-base ID appendix

## Source of truth
- Public: sanitized markdown only
- Private: JSON exports / ID appendix / Evidence Pack imports where applicable

## Integration notes
Cross-reference Airtable↔n8n: `../../CROSS_REFERENCE_AIRTABLE_N8N.md`

## Security
Never commit credentials. Prefer external secret stores / n8n credentials vault.
