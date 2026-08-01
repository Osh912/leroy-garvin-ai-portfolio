# Technical Documentation — GH-X MEO (Developers)

**Date:** 2026-07-20  
**Read-only analysis of live Airtable UI + cross-reference to n8n workflow definitions.**

## Stack role
Airtable = system of record / queue.  
n8n = external orchestrator (schedule → search → transform → API → update).  
OpenAI / HeyGen / Etsy / Metricool / Google Drive = side-effect systems via n8n HTTP/nodes.

## Table inventory
1. Products — product lifecycle + asset + publish + social SEO fields  
2. ContentQueue — per-platform content items linked to products  
3. Settings — key/value config  
4. Content Engine — script/video pipeline fields  
5. GHX Dashboard — goals/KPI snapshot  

## Suggested integration contracts (for implementers)
| Queue signal | Typical consumer | Writeback fields |
|--------------|------------------|------------------|
| Products Status / view Ready to Design | Image/mockup/product-file workflows | generated_image_url, google_drive_link, mockup_*, Error Log |
| Products publish-ready | Etsy draft publisher | etsy_listing_id, Publish Status, Error Log |
| ContentQueue Ready for Metricool | Metricool schedulers | Status, Scheduled Date, packs |
| Content Engine 01–03 views | Script builder / HeyGen create / poll | Script, video_*, heygen_error, Status |
| Settings keys | Any generator needing defaults | Read-only consumption |

## Field naming notes
Mix of Title Case (`Error Log`) and snake_case (`video_status`, `social_scheduled_at`) — consider normalizing (see schema improvements).

## Security
Treat Airtable API tokens and base/table IDs as secrets. Do not commit them to public repos.
