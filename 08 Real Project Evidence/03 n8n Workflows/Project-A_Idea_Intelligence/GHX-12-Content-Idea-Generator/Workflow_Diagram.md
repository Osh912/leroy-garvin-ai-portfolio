# Workflow Diagram — GHX-12-Content-Idea-Generator

**Source:** `GHX-12-Content-Idea-Generator.json` · **Status:** Functional Build · **Complexity:** Intermediate  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Daily_Content_Ideas["Schedule · Daily Content Ideas"]
  Set___Load_Content_Niches["Set · Load Content Niches"]
  Code___Setup_Config["Code · Setup Config"]
  Airtable___Search_Promotable_Products["Airtable · Search Promotable Products"]
  Code___Build_Daily_Ideas_Body["Code · Build Daily Ideas Body"]
  HTTP___OpenAI_Chat["HTTP · OpenAI Chat"]
  Code___Parse_Content_Ideas["Code · Parse Content Ideas"]
  Batch___Split_Ideas["Batch · Split Ideas"]
  Filter___Idea_OK["Filter · Idea OK"]
  Airtable___Create_Content_Row["Airtable · Create Content Row"]
  Code___Log_Skip["Code · Log Skip"]
  Code___Run_Complete["Code · Run Complete"]
  Schedule___Daily_Content_Ideas --> Set___Load_Content_Niches
  Set___Load_Content_Niches --> Code___Setup_Config
  Code___Setup_Config --> Airtable___Search_Promotable_Products
  Airtable___Search_Promotable_Products --> Code___Build_Daily_Ideas_Body
  Code___Build_Daily_Ideas_Body --> HTTP___OpenAI_Chat
  HTTP___OpenAI_Chat --> Code___Parse_Content_Ideas
  Code___Parse_Content_Ideas --> Batch___Split_Ideas
  Batch___Split_Ideas --> Filter___Idea_OK
  Batch___Split_Ideas --> Code___Run_Complete
  Filter___Idea_OK --> Airtable___Create_Content_Row
  Filter___Idea_OK --> Code___Log_Skip
  Airtable___Create_Content_Row --> Batch___Split_Ideas
  Code___Log_Skip --> Batch___Split_Ideas
```
