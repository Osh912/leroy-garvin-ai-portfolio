# Workflow Diagram — GHX-04-Mockup-Generator

**Source:** `GHX-04-Mockup-Generator.json` · **Status:** Functional Build · **Complexity:** Advanced  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Mockup_Run["Schedule · Mockup Run"]
  Airtable___Search_Mockup_Queue["Airtable · Search Mockup Queue"]
  Batch___Split_Records["Batch · Split Records"]
  Code___Build_Mockup_Chat_Body["Code · Build Mockup Chat Body"]
  HTTP___OpenAI_Chat["HTTP · OpenAI Chat"]
  Code___Parse_Mockup_Prompt["Code · Parse Mockup Prompt"]
  Filter___Prompt_OK["Filter · Prompt OK"]
  HTTP___OpenAI_Images["HTTP · OpenAI Images"]
  Code___Image_To_Binary["Code · Image To Binary"]
  Filter___Image_OK["Filter · Image OK"]
  Google_Drive___Upload_Mockup["Google Drive · Upload Mockup"]
  Code___Merge_Drive_Link["Code · Merge Drive Link"]
  Airtable___Update_Success["Airtable · Update Success"]
  Airtable___Update_Error["Airtable · Update Error"]
  Code___Batch_Complete["Code · Batch Complete"]
  Schedule___Mockup_Run --> Airtable___Search_Mockup_Queue
  Airtable___Search_Mockup_Queue --> Batch___Split_Records
  Batch___Split_Records --> Code___Build_Mockup_Chat_Body
  Batch___Split_Records --> Code___Batch_Complete
  Code___Build_Mockup_Chat_Body --> HTTP___OpenAI_Chat
  HTTP___OpenAI_Chat --> Code___Parse_Mockup_Prompt
  Code___Parse_Mockup_Prompt --> Filter___Prompt_OK
  Filter___Prompt_OK --> HTTP___OpenAI_Images
  Filter___Prompt_OK --> Airtable___Update_Error
  HTTP___OpenAI_Images --> Code___Image_To_Binary
  Code___Image_To_Binary --> Filter___Image_OK
  Filter___Image_OK --> Google_Drive___Upload_Mockup
  Filter___Image_OK --> Airtable___Update_Error
  Google_Drive___Upload_Mockup --> Code___Merge_Drive_Link
  Code___Merge_Drive_Link --> Airtable___Update_Success
  Airtable___Update_Success --> Batch___Split_Records
  Airtable___Update_Error --> Batch___Split_Records
```
