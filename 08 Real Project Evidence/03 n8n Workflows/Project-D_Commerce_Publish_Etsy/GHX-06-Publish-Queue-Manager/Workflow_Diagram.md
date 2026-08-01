# Workflow Diagram — GHX-06-Publish-Queue-Manager

**Source:** `GHX-06-Publish-Queue-Manager.json` · **Status:** Functional Build · **Complexity:** Intermediate  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Validation_Run["Schedule · Validation Run"]
  Airtable___Search_Ready_To_Publish["Airtable · Search Ready To Publish"]
  Batch___Split_Records["Batch · Split Records"]
  Code___Validate_Publish_Gate["Code · Validate Publish Gate"]
  Filter___Complete["Filter · Complete"]
  Airtable___Mark_Publish_Ready["Airtable · Mark Publish Ready"]
  Airtable___Append_Error_Log["Airtable · Append Error Log"]
  Code___Batch_Complete["Code · Batch Complete"]
  Schedule___Validation_Run --> Airtable___Search_Ready_To_Publish
  Airtable___Search_Ready_To_Publish --> Batch___Split_Records
  Batch___Split_Records --> Code___Validate_Publish_Gate
  Batch___Split_Records --> Code___Batch_Complete
  Code___Validate_Publish_Gate --> Filter___Complete
  Filter___Complete --> Airtable___Mark_Publish_Ready
  Filter___Complete --> Airtable___Append_Error_Log
  Airtable___Mark_Publish_Ready --> Batch___Split_Records
  Airtable___Append_Error_Log --> Batch___Split_Records
```
