# Workflow Diagram — GHX-14-Metricool-Content-Scheduler

**Source:** `GHX-14-Metricool-Content-Scheduler.json` · **Status:** Functional Build · **Complexity:** Advanced  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Metricool_Content_Run["Schedule · Metricool Content Run"]
  Set___Load_Metricool_Config["Set · Load Metricool Config"]
  Code___Setup_Config["Code · Setup Config"]
  Airtable___Search_Content_Queue["Airtable · Search Content Queue"]
  Batch___Split_Records["Batch · Split Records"]
  Code___Build_Metricool_Pack_Body["Code · Build Metricool Pack Body"]
  HTTP___OpenAI_Chat["HTTP · OpenAI Chat"]
  Code___Expand_Metricool_Posts["Code · Expand Metricool Posts"]
  Filter___Pack_OK["Filter · Pack OK"]
  Filter___API_Enabled["Filter · API Enabled"]
  HTTP___Metricool_Schedule_Post["HTTP · Metricool Schedule Post"]
  Code___Aggregate_Metricool_Results["Code · Aggregate Metricool Results"]
  Filter___Schedule_OK["Filter · Schedule OK"]
  Airtable___Save_Post_Pack["Airtable · Save Post Pack"]
  Airtable___Log_Scheduler_Error["Airtable · Log Scheduler Error"]
  Code___Batch_Complete["Code · Batch Complete"]
  Schedule___Metricool_Content_Run --> Set___Load_Metricool_Config
  Set___Load_Metricool_Config --> Code___Setup_Config
  Code___Setup_Config --> Airtable___Search_Content_Queue
  Airtable___Search_Content_Queue --> Batch___Split_Records
  Batch___Split_Records --> Code___Build_Metricool_Pack_Body
  Batch___Split_Records --> Code___Batch_Complete
  Code___Build_Metricool_Pack_Body --> HTTP___OpenAI_Chat
  HTTP___OpenAI_Chat --> Code___Expand_Metricool_Posts
  Code___Expand_Metricool_Posts --> Filter___Pack_OK
  Filter___Pack_OK --> Filter___API_Enabled
  Filter___Pack_OK --> Airtable___Log_Scheduler_Error
  Filter___API_Enabled --> HTTP___Metricool_Schedule_Post
  Filter___API_Enabled --> Airtable___Save_Post_Pack
  HTTP___Metricool_Schedule_Post --> Code___Aggregate_Metricool_Results
  Code___Aggregate_Metricool_Results --> Filter___Schedule_OK
  Filter___Schedule_OK --> Airtable___Save_Post_Pack
  Filter___Schedule_OK --> Airtable___Log_Scheduler_Error
  Airtable___Save_Post_Pack --> Batch___Split_Records
  Airtable___Log_Scheduler_Error --> Batch___Split_Records
```
