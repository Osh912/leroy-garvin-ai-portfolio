# Workflow Diagram — GHX-10-Performance-Tracker

**Source:** `GHX-10-Performance-Tracker.json` · **Status:** Functional Build · **Complexity:** Advanced  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Weekly_Metrics["Schedule · Weekly Metrics"]
  Airtable___Search_Live_Products["Airtable · Search Live Products"]
  Batch___Split_Records["Batch · Split Records"]
  Code___Prep_Metrics_Context["Code · Prep Metrics Context"]
  Filter___Has_Etsy_Listing["Filter · Has Etsy Listing"]
  HTTP___Etsy_Get_Listing["HTTP · Etsy Get Listing"]
  Code___Score_Metrics["Code · Score Metrics"]
  Code___Score_Without_Etsy["Code · Score Without Etsy"]
  HTTP___OpenAI_Notes["HTTP · OpenAI Notes"]
  Code___Merge_AI_Notes["Code · Merge AI Notes"]
  Airtable___Save_Metrics["Airtable · Save Metrics"]
  Code___Batch_Complete["Code · Batch Complete"]
  Schedule___Weekly_Metrics --> Airtable___Search_Live_Products
  Airtable___Search_Live_Products --> Batch___Split_Records
  Batch___Split_Records --> Code___Prep_Metrics_Context
  Batch___Split_Records --> Code___Batch_Complete
  Code___Prep_Metrics_Context --> Filter___Has_Etsy_Listing
  Filter___Has_Etsy_Listing --> HTTP___Etsy_Get_Listing
  Filter___Has_Etsy_Listing --> Code___Score_Without_Etsy
  HTTP___Etsy_Get_Listing --> Code___Score_Metrics
  Code___Score_Metrics --> HTTP___OpenAI_Notes
  Code___Score_Without_Etsy --> HTTP___OpenAI_Notes
  HTTP___OpenAI_Notes --> Code___Merge_AI_Notes
  Code___Merge_AI_Notes --> Airtable___Save_Metrics
  Airtable___Save_Metrics --> Batch___Split_Records
```
