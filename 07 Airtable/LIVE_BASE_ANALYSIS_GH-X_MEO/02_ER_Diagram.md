# ER Diagram — GH-X MEO

```mermaid
erDiagram
  PRODUCTS ||--o{{ CONTENT_QUEUE : "has content items" }}
  PRODUCTS ||--o{{ CONTENT_ENGINE : "product link / related content (Needs Review)" }}
  SETTINGS ||--|| SETTINGS : "key-value config (standalone)"
  GHX_DASHBOARD ||--|| GHX_DASHBOARD : "KPI snapshot (standalone)"

  PRODUCTS {{
    string Name PK
    string Status
    string Publish_Status
    string qa_status
    string social_status
    string mockup_status
    number Price
    string Error_Log
    string etsy_listing_id
    string google_drive_link
    string generated_image_url
  }}

  CONTENT_QUEUE {{
    string Content_ID PK
    string Product FK
    string Platform
    string Status
    datetime Scheduled_Date
    string Media_File_URL
  }}

  CONTENT_ENGINE {{
    string Name PK
    string Status
    string Platform
    string video_status
    string video_id
    string video_url
    string heygen_error
    string Metricool_Post_Pack
  }}

  SETTINGS {{
    string Key PK
    string Value
    string Notes
  }}

  GHX_DASHBOARD {{
    string Name PK
    number Products_Ready
    number Video_Ready
    number Scheduled_Posts
    number Posted_Today
    number Pending_Videos
    number Revenue
    number Daily_Product_Goal
    number Daily_Video_Goal
    number Monthly_Revenue_Goal
  }}
```

**Needs Review:** Confirm whether Content Engine uses a true linked-record field to Products vs URL-only Product Link.
