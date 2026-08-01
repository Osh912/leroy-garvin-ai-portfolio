# Workflow Diagram — GHX-16-HeyGen-Video-Generator

**Source:** `GHX-16-HeyGen-Video-Generator.json` · **Status:** Functional Build · **Complexity:** Intermediate  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Every_15_Minutes["Schedule · Every 15 Minutes"]
  Set___Load_HeyGen_Config["Set · Load HeyGen Config"]
  Code___Setup_Config["Code · Setup Config"]
  Airtable___Search_Video_Ready["Airtable · Search Video Ready"]
  Batch___Split_Records["Batch · Split Records"]
  Code___Build_HeyGen_Payload["Code · Build HeyGen Payload"]
  Filter___Payload_OK["Filter · Payload OK"]
  HTTP___HeyGen_Create_Video["HTTP · HeyGen Create Video"]
  Code___Parse_HeyGen_Response["Code · Parse HeyGen Response"]
  Filter___Video_Id_Returned["Filter · Video Id Returned"]
  Airtable___Mark_Video_Processing["Airtable · Mark Video Processing"]
  Airtable___Log_HeyGen_Error["Airtable · Log HeyGen Error"]
  Code___Batch_Complete["Code · Batch Complete"]
  Schedule___Every_15_Minutes --> Set___Load_HeyGen_Config
  Set___Load_HeyGen_Config --> Code___Setup_Config
  Code___Setup_Config --> Airtable___Search_Video_Ready
  Airtable___Search_Video_Ready --> Batch___Split_Records
  Batch___Split_Records --> Code___Build_HeyGen_Payload
  Batch___Split_Records --> Code___Batch_Complete
  Code___Build_HeyGen_Payload --> Filter___Payload_OK
  Filter___Payload_OK --> HTTP___HeyGen_Create_Video
  Filter___Payload_OK --> Airtable___Log_HeyGen_Error
  HTTP___HeyGen_Create_Video --> Code___Parse_HeyGen_Response
  Code___Parse_HeyGen_Response --> Filter___Video_Id_Returned
  Filter___Video_Id_Returned --> Airtable___Mark_Video_Processing
  Filter___Video_Id_Returned --> Airtable___Log_HeyGen_Error
  Airtable___Mark_Video_Processing --> Batch___Split_Records
  Airtable___Log_HeyGen_Error --> Batch___Split_Records
```
