# Developer Documentation — AI Voice Booking Assistant

## Stack touchpoints
- AI: Conversational prompt/stage logic (ChatGPT/Claude used in design docs)
- APIs: Documented concept-level Twilio/Airtable/n8n references — live credentials not published; telephony config Evidence Pending
- Airtable: Planned booking structures in 07 docs; live GH-X MEO is product ops (separate). Voice-specific live base Evidence Pending

## Source of truth
- Public: sanitized markdown only
- Private: JSON exports / ID appendix / Evidence Pack imports where applicable

## Integration notes
Cross-reference Airtable↔n8n: `../../CROSS_REFERENCE_AIRTABLE_N8N.md`

## Security
Never commit credentials. Prefer external secret stores / n8n credentials vault.
