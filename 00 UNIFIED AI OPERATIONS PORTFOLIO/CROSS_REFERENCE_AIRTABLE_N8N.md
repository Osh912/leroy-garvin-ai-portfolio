# CROSS_REFERENCE_AIRTABLE_N8N.md

**Updated:** 2026-07-20

Canonical workflows only (Desktop). Airtable target: **GH-X MEO** live schema.

| Workflow | Airtable focus | Fields / signals (observed or inferred) | n8n Airtable ops pattern |
|----------|----------------|------------------------------------------|--------------------------|
| Design + Reel Prompt Generator | Products | Reel Prompt / Cover Prompt fields | Search + Update |
| GH-X OpenAI Image Generator | Products | generated_image_url, google_drive_link, Cover Image URL, Error Log | Search + Update + Drive |
| GHX-00-Error-Alerts | n/a (Error Trigger) | May alert outside Airtable; destination Needs Review | Error Trigger + HTTP |
| GHX-01-Idea-Intelligence | Products | Creates product idea rows; Status/Priority fields | Airtable Create |
| GHX-03-Etsy-Metricool-Handoff | Products | Etsy Listing Draft / handoff fields | Search + Update |
| GHX-03B-Product-File-Uploader | Products | Product File URL, Design Instructions, Error Log | Search + Update |
| GHX-04-Mockup-Generator | Products | mockup_status, mockup_prompt, mockup_image_url, Mockup URLs | Search + Update + Drive |
| GHX-05-Social-Asset-Generator | Products / ContentQueue | captions, hashtags, social_status | Search + Update |
| GHX-06-Publish-Queue-Manager | Products | Publish Status validation / Error Log | Search + Update |
| GHX-07-Etsy-Draft-Publisher | Products | etsy_listing_id, Publish Status, Upload Pack Sent?, Error Log | Search + Update + Etsy HTTP |
| GHX-07-Performance-Tracker | Products | Performance Notes, winner_score, Recommended Action | Search + Update |
| GHX-08-Metricool-Scheduler | Products / ContentQueue | Metricool Post Pack, social_scheduled_at, social_status | Search + Update + Metricool |
| GHX-09-Ready-To-Post-Queue | ContentQueue | Scheduled → Ready/Posted queue rows | Search + Create/Update |
| GHX-09-Self-Healing-QA | Products / Content Engine | Error Log / failed rows requeue | Search + Update |
| GHX-10-Performance-Tracker | Products | Live Products + etsy_listing_id metrics notes | Search + Update + Etsy |
| GHX-11-Winning-Idea-Loop | Products | Reads winner_score / Performance Notes; creates idea rows | Search + Create |
| GHX-12-Content-Idea-Generator | Products / ContentQueue | Promotable products → content ideas | Search + Create |
| GHX-13-Video-Script-Builder | Content Engine | Script queue views; Hook/Script/CTA | Search + Update |
| GHX-14-Metricool-Content-Scheduler | ContentQueue / Content Engine | Ready for Metricool views; packs | Search + Update + Metricool |
| GHX-15-Content-QA | Content Engine / Products | qa_status / needs_fix / video_ready views | Search + Update |
| GHX-16-HeyGen-Video-Generator | Content Engine | video_id, video_status, heygen_error | Search + Update + HeyGen |
| GHX-17-HeyGen-Status-Poller | Content Engine | video_status polling; video_url; Status | Search + Update + HeyGen |
| GHX-Generate-Product-Listing | Products | Title/Description/Tags/seo_* updates; Error Log | Search + Update |

## Settings consumption
- `default_price`, `default_platforms`, `daily_product_limit`, `daily_content_per_product`, `brand_voice` may feed generator workflows (Needs Review which exact workflows read Settings table).

## Non-claims
Field mappings are based on live schema names + workflow definition purposes. Exact filter formulas inside n8n nodes are private JSON detail and not republished here.
