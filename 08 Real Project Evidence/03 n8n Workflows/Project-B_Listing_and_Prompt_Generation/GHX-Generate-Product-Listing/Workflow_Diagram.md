# Workflow Diagram — GHX-Generate-Product-Listing

**Source:** `GHX-Generate-Product-Listing.json` · **Status:** Functional Build · **Complexity:** Intermediate  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Listing_Run["Schedule · Listing Run"]
  Airtable___Search_Ideas["Airtable · Search Ideas"]
  Batch___Split_Records["Batch · Split Records"]
  Code___Build_Chat_Payload["Code · Build Chat Payload"]
  HTTP___OpenAI_Chat["HTTP · OpenAI Chat"]
  Code___Parse_Listing_JSON["Code · Parse Listing JSON"]
  Filter___Parse_OK["Filter · Parse OK"]
  Airtable___Update_Success["Airtable · Update Success"]
  Airtable___Update_Error["Airtable · Update Error"]
  Code___Batch_Complete["Code · Batch Complete"]
  Schedule___Listing_Run --> Airtable___Search_Ideas
  Airtable___Search_Ideas --> Batch___Split_Records
  Batch___Split_Records --> Code___Build_Chat_Payload
  Batch___Split_Records --> Code___Batch_Complete
  Code___Build_Chat_Payload --> HTTP___OpenAI_Chat
  HTTP___OpenAI_Chat --> Code___Parse_Listing_JSON
  Code___Parse_Listing_JSON --> Filter___Parse_OK
  Filter___Parse_OK --> Airtable___Update_Success
  Filter___Parse_OK --> Airtable___Update_Error
  Airtable___Update_Success --> Batch___Split_Records
  Airtable___Update_Error --> Batch___Split_Records
```
