# Workflow Diagram — GHX-08-Metricool-Scheduler

**Source:** `GHX-08-Metricool-Scheduler.json` · **Status:** Functional Build · **Complexity:** Advanced  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Social_Schedule_Run["Schedule · Social Schedule Run"]
  Set___Load_Metricool_Config["Set · Load Metricool Config"]
  Code___Setup_Config["Code · Setup Config"]
  Airtable___Search_Social_Queue["Airtable · Search Social Queue"]
  Batch___Split_Records["Batch · Split Records"]
  Code___Build_Caption_Body["Code · Build Caption Body"]
  HTTP___OpenAI_Chat["HTTP · OpenAI Chat"]
  Code___Expand_Platform_Posts["Code · Expand Platform Posts"]
  Filter___API_Enabled["Filter · API Enabled"]
  HTTP___Metricool_Schedule_Post["HTTP · Metricool Schedule Post"]
  Code___Aggregate_Schedule_Results["Code · Aggregate Schedule Results"]
  Filter___Schedule_OK["Filter · Schedule OK"]
  Airtable___Mark_Scheduled["Airtable · Mark Scheduled"]
  Airtable___Log_Schedule_Error["Airtable · Log Schedule Error"]
  Airtable___Save_Dry_Run_Post_Pack["Airtable · Save Dry Run Post Pack"]
  Code___Batch_Complete["Code · Batch Complete"]
  Schedule___Social_Schedule_Run --> Set___Load_Metricool_Config
  Set___Load_Metricool_Config --> Code___Setup_Config
  Code___Setup_Config --> Airtable___Search_Social_Queue
  Airtable___Search_Social_Queue --> Batch___Split_Records
  Batch___Split_Records --> Code___Build_Caption_Body
  Batch___Split_Records --> Code___Batch_Complete
  Code___Build_Caption_Body --> HTTP___OpenAI_Chat
  HTTP___OpenAI_Chat --> Code___Expand_Platform_Posts
  Code___Expand_Platform_Posts --> Filter___API_Enabled
  Filter___API_Enabled --> HTTP___Metricool_Schedule_Post
  Filter___API_Enabled --> Airtable___Save_Dry_Run_Post_Pack
  HTTP___Metricool_Schedule_Post --> Code___Aggregate_Schedule_Results
  Code___Aggregate_Schedule_Results --> Filter___Schedule_OK
  Filter___Schedule_OK --> Airtable___Mark_Scheduled
  Filter___Schedule_OK --> Airtable___Log_Schedule_Error
  Airtable___Mark_Scheduled --> Batch___Split_Records
  Airtable___Log_Schedule_Error --> Batch___Split_Records
  Airtable___Save_Dry_Run_Post_Pack --> Batch___Split_Records
```
