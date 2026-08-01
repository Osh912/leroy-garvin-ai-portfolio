# Workflow Diagram — GHX-17-HeyGen-Status-Poller

**Source:** `GHX-17-HeyGen-Status-Poller.json` · **Status:** Functional Build · **Complexity:** Intermediate  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Every_10_Minutes["Schedule · Every 10 Minutes"]
  Airtable___Search_Processing_Videos["Airtable · Search Processing Videos"]
  Batch___Split_Records["Batch · Split Records"]
  Code___Prepare_Poll_Context["Code · Prepare Poll Context"]
  Filter___Context_OK["Filter · Context OK"]
  HTTP___HeyGen_Get_Status["HTTP · HeyGen Get Status"]
  Code___Parse_HeyGen_Status["Code · Parse HeyGen Status"]
  Switch___HeyGen_Status["Switch · HeyGen Status"]
  Airtable___Mark_Ready_To_Schedule["Airtable · Mark Ready To Schedule"]
  Code___Log_Still_Processing["Code · Log Still Processing"]
  Airtable___Mark_Video_Failed["Airtable · Mark Video Failed"]
  Airtable___Log_Poll_Error["Airtable · Log Poll Error"]
  Airtable___Log_Context_Error["Airtable · Log Context Error"]
  Code___Batch_Complete["Code · Batch Complete"]
  Schedule___Every_10_Minutes --> Airtable___Search_Processing_Videos
  Airtable___Search_Processing_Videos --> Batch___Split_Records
  Batch___Split_Records --> Code___Prepare_Poll_Context
  Batch___Split_Records --> Code___Batch_Complete
  Code___Prepare_Poll_Context --> Filter___Context_OK
  Filter___Context_OK --> HTTP___HeyGen_Get_Status
  Filter___Context_OK --> Airtable___Log_Context_Error
  HTTP___HeyGen_Get_Status --> Code___Parse_HeyGen_Status
  Code___Parse_HeyGen_Status --> Switch___HeyGen_Status
  Switch___HeyGen_Status --> Airtable___Mark_Ready_To_Schedule
  Switch___HeyGen_Status --> Code___Log_Still_Processing
  Switch___HeyGen_Status --> Airtable___Mark_Video_Failed
  Switch___HeyGen_Status --> Airtable___Log_Poll_Error
  Airtable___Mark_Ready_To_Schedule --> Batch___Split_Records
  Code___Log_Still_Processing --> Batch___Split_Records
  Airtable___Mark_Video_Failed --> Batch___Split_Records
  Airtable___Log_Poll_Error --> Batch___Split_Records
  Airtable___Log_Context_Error --> Batch___Split_Records
```
