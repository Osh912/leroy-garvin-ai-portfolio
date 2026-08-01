# Workflow Diagram — GHX-05-Social-Asset-Generator

**Source:** `GHX-05-Social-Asset-Generator.json` · **Status:** Functional Build · **Complexity:** Intermediate  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Social_Run["Schedule · Social Run"]
  Airtable___Search_Social_Queue["Airtable · Search Social Queue"]
  Batch___Split_Records["Batch · Split Records"]
  Code___Build_Social_Chat_Body["Code · Build Social Chat Body"]
  HTTP___OpenAI_Chat["HTTP · OpenAI Chat"]
  Code___Parse_Social_JSON["Code · Parse Social JSON"]
  Filter___Parse_OK["Filter · Parse OK"]
  Airtable___Update_Success["Airtable · Update Success"]
  Airtable___Update_Error["Airtable · Update Error"]
  Code___Batch_Complete["Code · Batch Complete"]
  Schedule___Social_Run --> Airtable___Search_Social_Queue
  Airtable___Search_Social_Queue --> Batch___Split_Records
  Batch___Split_Records --> Code___Build_Social_Chat_Body
  Batch___Split_Records --> Code___Batch_Complete
  Code___Build_Social_Chat_Body --> HTTP___OpenAI_Chat
  HTTP___OpenAI_Chat --> Code___Parse_Social_JSON
  Code___Parse_Social_JSON --> Filter___Parse_OK
  Filter___Parse_OK --> Airtable___Update_Success
  Filter___Parse_OK --> Airtable___Update_Error
  Airtable___Update_Success --> Batch___Split_Records
  Airtable___Update_Error --> Batch___Split_Records
```
