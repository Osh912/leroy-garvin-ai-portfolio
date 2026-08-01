# Complete Table Documentation — GH-X MEO (Live Base)

**Analysis date:** 2026-07-20  
**Base name:** GH-X MEO  
**Method:** Read-only browser inspection of Airtable UI  
**Scope note:** This documents the **GH-X MEO** base currently open/recent in Airtable. Other workspace bases (e.g., GH-X Product Tracker, Ro Picks Engine) were listed on Home but **not** fully analyzed in this pass — Needs Review if required.  
**Rule:** No records or fields were modified.  
**Privacy:** Base/table/view IDs are stored only in the private appendix file. Do not publish IDs publicly.

## Base overview
GH-X MEO is the operational Airtable system supporting GH-X digital product automation: product ideation → design/assets → publish → social/video content → KPI snapshot settings.

Native Airtable **Automations:** none configured (empty catalog / “Add trigger” state observed).  
Native Airtable **Forms:** none configured (empty Forms hub observed).  
Native Airtable **Interfaces hub:** empty onboarding UI observed; operational “interfaces” in sidebar are actually **tables** named Content Engine and GHX Dashboard.

## Tables (5)

### 1. Products (primary product queue)
**Purpose:** Master queue for digital products through idea → design → upload → live stages.

**Views observed**
| View | Likely role |
|------|-------------|
| Grid view | Full table |
| Ideas | Early-stage ideas |
| Ready to Design | Design queue |
| Ready to Upload | Upload/publish prep |
| Live Products | Live listings |

**Fields observed (names)**
| Field | Inferred type (Needs Review if exact type differs) | Role |
|-------|-----------------------------------------------------|------|
| Name | Primary text | Product label |
| Niche | Text / select | Category |
| Product Type | Text / select | Type (e.g., Journal) |
| Target Platforms | Text / multi-select | Sales channels |
| Status | Select | Pipeline status |
| Priority | Select / number | Prioritization |
| Title | Text | Listing title |
| Description | Long text | Listing body |
| Tags | Text / multi | SEO/tags |
| Price | Currency/number | Price |
| Design Instructions | Long text | Creative brief |
| Product File URL | URL | Deliverable file |
| Cover Image URL | URL | Cover asset |
| Upload Pack Sent? | Checkbox | Ops flag |
| Interior PDF URL | URL | Interior asset |
| Mockup URLs | URL / text | Mockup assets |
| Canva Design ID | Text | Design tool ID |
| Publish Status | Select | Publish state |
| Error Log | Long text | Failure notes for n8n/ops |
| Updated At | Date/time | Audit |
| Created At | Date/time | Audit |
| ContentQueue | Linked record (to ContentQueue) **Needs Review confirm** | Related social rows |
| Reel Prompt | Long text | Prompt artifact |
| Cover Prompt | Long text | Prompt artifact |
| Reel Script | Long text | Script artifact |
| Cover Image Link | URL | Asset |
| Etsy Listing Draft | Long text / object text | Draft payload |
| Metricool Post Pack | Long text | Social pack |
| generated_image_url | URL | AI image |
| google_drive_link | URL | Drive storage |
| seo_title | Text | SEO |
| seo_tags | Text | SEO |
| mockup_status | Select | Mockup stage |
| mockup_prompt | Long text | Mockup prompt |
| mockup_image_url | URL | Mockup asset |
| pinterest_caption | Long text | Social copy |
| tiktok_hook | Text/long text | Social hook |
| hashtags | Text | Social |
| social_status | Select | Social stage |
| instagram_caption | Long text | Social copy |
| published_draft | Checkbox/text | Draft flag |
| etsy_listing_id | Text | External ID |
| qa_status | Select | QA gate |
| winner_score | Number | Performance score |
| Performance Notes | Long text | Metrics notes |
| Recommended Action | Long text | Next action |
| social_scheduled_at | Date/time | Schedule |

**Record volume (observed):** at least ~18 product rows visible in Grid view (exact total Needs Review).

---

### 2. ContentQueue
**Purpose:** Social content items linked to products for Metricool/scheduling style workflows.

**Views observed:** Grid view, To Create, Ready for Metricool, Scheduled, Posted  
**Note:** One viewed state showed “0 contents / All records are filtered” — other views may contain rows (Needs Review).

**Fields observed**
| Field | Inferred type | Role |
|-------|---------------|------|
| Content ID | Primary/text | Content key |
| Product | Linked record → Products | Relationship |
| Platform | Select/text | Channel |
| Format | Select/text | Format |
| Hook | Text/long text | Hook |
| Script or Text | Long text | Body |
| Caption | Long text | Caption |
| Hashtags | Text | Tags |
| CTA | Text | Call to action |
| Status | Select | Queue status |
| Scheduled Date | Date | Schedule |
| Media File URL | URL | Media |
| Notes | Long text | Notes |
| Created At | Date/time | Audit |

---

### 3. Settings
**Purpose:** Key/value operational configuration for automation defaults.

**Views:** Grid view  
**Fields:** Key · Value · Notes  
**Keys observed**
| Key | Example value (config, not secret) | Notes |
|-----|--------------------------------------|-------|
| default_price | 4.99 | Default listing price |
| default_platforms | Etsy, Shopify | Default platforms |
| daily_product_limit | 3 | Throughput control |
| daily_content_per_product | 5 | Content volume control |
| brand_voice | Brand voice string for Aligned Vibes Co | Prompt/brand guidance |

---

### 4. Content Engine
**Purpose:** Video/script content pipeline (HeyGen-oriented fields present).

**Views observed**
- Grid view
- 01 Script queue
- 02 Script built
- 03 Video ready
- 04 Needs fix
- 05 By platform
- 06 Ready for Metricool

**Fields observed**
| Field | Role |
|-------|------|
| Name | Primary |
| Notes | Notes |
| Assignee | Person/text |
| Status | Pipeline status (e.g., needs_fix, video_ready observed in UI) |
| Attachments | Files |
| Attachment Summary | Summary |
| Hook / Script / CTA | Creative fields |
| Platform / Video Type | Channel/type |
| Caption / Hashtags | Social |
| Product Link | URL / link |
| Platform Scripts Pack | Pack text |
| Metricool Post Pack | Pack text |
| Error Log | Errors |
| Created At | Audit |
| social_status | Social state |
| Posted At | Posted time |
| video_url / video_id / video_status | HeyGen/video artifacts |
| Post URL | Published URL |
| heygen_error | HeyGen error text |
| needs_fix | Fix flag/status |

**Volume:** dozens of rows visible (exact count Needs Review).

---

### 5. GHX Dashboard
**Purpose:** Single-row KPI / goals snapshot (“GH-X HQ”).

**Fields observed**
| Field | Role |
|-------|------|
| Name | Dashboard name |
| Products Ready | Count metric |
| Video Ready | Count metric |
| Scheduled Posts | Count metric |
| Posted Today | Count metric |
| Pending Videos | Count metric |
| Revenue | Currency metric |
| Daily Product Goal | Goal |
| Daily Video Goal | Goal |
| Monthly Revenue Goal | Goal |

**Records:** 1 observed (“GH-X HQ”). Metric sums mostly 0 except goals (10 / 3 / 5000) at inspection time — **not** claimed as business performance proof.

---

## Relationships (logical)
- ContentQueue.Product → Products (linked)
- Products.ContentQueue → ContentQueue (reverse link likely)
- Content Engine.Product Link → likely Products URL or link field (exact link type Needs Review)
- Settings is standalone config (no observed links)
- GHX Dashboard is standalone KPI row (may be formula/manual; Needs Review whether formulas roll up from other tables)

## Automations / Interfaces / Forms
| Area | Observation |
|------|-------------|
| Airtable Automations | No custom automations found; suggestions only |
| Forms | No custom forms found |
| Interfaces (top nav hub) | Empty onboarding; operational UIs are tables Content Engine + GHX Dashboard |

## n8n connection (from prior workflow definition analysis + this schema)
n8n workflows search/update Airtable queues using Status/Publish Status/Error Log/URL fields on Products and related content tables — matching this base’s field names (Error Log, google_drive_link, mockup_*, etsy_listing_id, video_*, Metricool Post Pack, etc.).
