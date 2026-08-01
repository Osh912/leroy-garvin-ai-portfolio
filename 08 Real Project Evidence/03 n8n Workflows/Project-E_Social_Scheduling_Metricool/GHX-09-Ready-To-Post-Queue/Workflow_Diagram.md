# Workflow Diagram — GHX-09-Ready-To-Post-Queue

**Source:** `GHX-09-Ready-To-Post-Queue.json` · **Status:** Functional Build · **Complexity:** Intermediate  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Every_Hour["Schedule · Every Hour"]
  Code___Reset_Run_Counters["Code · Reset Run Counters"]
  Airtable___Search_Scheduled_Content["Airtable · Search Scheduled Content"]
  Batch___Split_Records["Batch · Split Records"]
  Code___Build_Ready_To_Post_Queue_Items["Code · Build Ready-To-Post Queue Items"]
  Filter___Queue_Item_OK["Filter · Queue Item OK"]
  Airtable___Create_Ready_To_Post_Row["Airtable · Create Ready To Post Row"]
  Airtable___Mark_Queued_To_Post["Airtable · Mark Queued To Post"]
  Code___Log_Queued_Item["Code · Log Queued Item"]
  Code___Log_Skipped_Item["Code · Log Skipped Item"]
  Code___Run_Summary["Code · Run Summary"]
  Schedule___Every_Hour --> Code___Reset_Run_Counters
  Code___Reset_Run_Counters --> Airtable___Search_Scheduled_Content
  Airtable___Search_Scheduled_Content --> Batch___Split_Records
  Batch___Split_Records --> Code___Build_Ready_To_Post_Queue_Items
  Batch___Split_Records --> Code___Run_Summary
  Code___Build_Ready_To_Post_Queue_Items --> Filter___Queue_Item_OK
  Filter___Queue_Item_OK --> Airtable___Create_Ready_To_Post_Row
  Filter___Queue_Item_OK --> Code___Log_Skipped_Item
  Airtable___Create_Ready_To_Post_Row --> Airtable___Mark_Queued_To_Post
  Airtable___Mark_Queued_To_Post --> Code___Log_Queued_Item
  Code___Log_Queued_Item --> Batch___Split_Records
  Code___Log_Skipped_Item --> Batch___Split_Records
```
