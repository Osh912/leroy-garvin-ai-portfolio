# GH-X MEO Airtable — Public Summary

**Date:** 2026-07-20

Sanitized summary of the live **GH-X MEO** base used as the GH-X operations data layer.

## Tables (names only)
1. **Products** — product lifecycle queue (ideas → design → upload → live) with asset URLs, publish/QA/social statuses, error log  
2. **ContentQueue** — social content items linked to products  
3. **Settings** — defaults (price, platforms, daily limits, brand voice)  
4. **Content Engine** — script/video content pipeline with platform views  
5. **GHX Dashboard** — goals/KPI snapshot row  

## Relationships
Products ↔ ContentQueue (linked). Content Engine relates to products via product link fields (exact link type Needs Review). Settings and Dashboard are standalone config/KPI tables.

## Automation note
Native Airtable Automations/Forms were empty at inspection. Orchestration is designed around external **n8n** workflows updating Airtable statuses and artifact fields.

## Evidence / claims
- Schema observed live  
- No production volume/revenue claims from dashboard values  
- Base/table IDs and record contents withheld from public pack  

See also: [README](./README.md) in this folder for the broader Airtable case study.
