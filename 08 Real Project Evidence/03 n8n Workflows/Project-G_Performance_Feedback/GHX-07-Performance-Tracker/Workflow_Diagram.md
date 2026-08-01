# Workflow Diagram — GHX-07-Performance-Tracker

**Source:** `GHX-07-Performance-Tracker.json` · **Status:** Functional Build · **Complexity:** Intermediate  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Weekly_Performance["Schedule · Weekly Performance"]
  Airtable___Search_Published["Airtable · Search Published"]
  Batch___Split_Records["Batch · Split Records"]
  Code___Score_Metrics["Code · Score Metrics"]
  HTTP___OpenAI_Chat["HTTP · OpenAI Chat"]
  Code___Merge_AI_Notes["Code · Merge AI Notes"]
  Airtable___Save_Metrics["Airtable · Save Metrics"]
  Code___Batch_Complete["Code · Batch Complete"]
  Schedule___Weekly_Performance --> Airtable___Search_Published
  Airtable___Search_Published --> Batch___Split_Records
  Batch___Split_Records --> Code___Score_Metrics
  Batch___Split_Records --> Code___Batch_Complete
  Code___Score_Metrics --> HTTP___OpenAI_Chat
  HTTP___OpenAI_Chat --> Code___Merge_AI_Notes
  Code___Merge_AI_Notes --> Airtable___Save_Metrics
  Airtable___Save_Metrics --> Batch___Split_Records
```
