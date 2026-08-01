# Workflow Diagram — GHX-13-Video-Script-Builder

**Source:** `GHX-13-Video-Script-Builder.json` · **Status:** Functional Build · **Complexity:** Intermediate  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Script_Build_Run["Schedule · Script Build Run"]
  Airtable___Search_Script_Queue["Airtable · Search Script Queue"]
  Batch___Split_Records["Batch · Split Records"]
  Code___Build_Script_Body["Code · Build Script Body"]
  HTTP___OpenAI_Chat["HTTP · OpenAI Chat"]
  Code___Parse_Platform_Scripts["Code · Parse Platform Scripts"]
  Filter___Script_OK["Filter · Script OK"]
  Airtable___Save_Scripts["Airtable · Save Scripts"]
  Airtable___Log_Script_Error["Airtable · Log Script Error"]
  Code___Batch_Complete["Code · Batch Complete"]
  Schedule___Script_Build_Run --> Airtable___Search_Script_Queue
  Airtable___Search_Script_Queue --> Batch___Split_Records
  Batch___Split_Records --> Code___Build_Script_Body
  Batch___Split_Records --> Code___Batch_Complete
  Code___Build_Script_Body --> HTTP___OpenAI_Chat
  HTTP___OpenAI_Chat --> Code___Parse_Platform_Scripts
  Code___Parse_Platform_Scripts --> Filter___Script_OK
  Filter___Script_OK --> Airtable___Save_Scripts
  Filter___Script_OK --> Airtable___Log_Script_Error
  Airtable___Save_Scripts --> Batch___Split_Records
  Airtable___Log_Script_Error --> Batch___Split_Records
```
