# Workflow Diagram — GHX-07-Etsy-Draft-Publisher

**Source:** `GHX-07-Etsy-Draft-Publisher.json` · **Status:** Functional Build · **Complexity:** Advanced  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Etsy_Draft_Run["Schedule · Etsy Draft Run"]
  Set___Load_Env_Config["Set · Load Env Config"]
  Code___Setup_Config["Code · Setup Config"]
  Airtable___Search_Publish_Queue["Airtable · Search Publish Queue"]
  Batch___Split_Records["Batch · Split Records"]
  Code___Build_Etsy_Payload["Code · Build Etsy Payload"]
  Filter___Preflight_OK["Filter · Preflight OK"]
  HTTP___Etsy_Create_Draft["HTTP · Etsy Create Draft"]
  Code___Parse_Listing_Id["Code · Parse Listing Id"]
  Filter___Listing_Created["Filter · Listing Created"]
  HTTP___Download_Mockup["HTTP · Download Mockup"]
  HTTP___Etsy_Upload_Image["HTTP · Etsy Upload Image"]
  HTTP___Download_Digital_File["HTTP · Download Digital File"]
  HTTP___Etsy_Upload_Digital_File["HTTP · Etsy Upload Digital File"]
  Code___Build_Success_Payload["Code · Build Success Payload"]
  Airtable___Save_Etsy_Draft["Airtable · Save Etsy Draft"]
  Airtable___Log_Etsy_Error["Airtable · Log Etsy Error"]
  Code___Batch_Complete["Code · Batch Complete"]
  Schedule___Etsy_Draft_Run --> Set___Load_Env_Config
  Set___Load_Env_Config --> Code___Setup_Config
  Code___Setup_Config --> Airtable___Search_Publish_Queue
  Airtable___Search_Publish_Queue --> Batch___Split_Records
  Batch___Split_Records --> Code___Build_Etsy_Payload
  Batch___Split_Records --> Code___Batch_Complete
  Code___Build_Etsy_Payload --> Filter___Preflight_OK
  Filter___Preflight_OK --> HTTP___Etsy_Create_Draft
  Filter___Preflight_OK --> Airtable___Log_Etsy_Error
  HTTP___Etsy_Create_Draft --> Code___Parse_Listing_Id
  Code___Parse_Listing_Id --> Filter___Listing_Created
  Filter___Listing_Created --> HTTP___Download_Mockup
  Filter___Listing_Created --> Airtable___Log_Etsy_Error
  HTTP___Download_Mockup --> HTTP___Etsy_Upload_Image
  HTTP___Etsy_Upload_Image --> HTTP___Download_Digital_File
  HTTP___Download_Digital_File --> HTTP___Etsy_Upload_Digital_File
  HTTP___Etsy_Upload_Digital_File --> Code___Build_Success_Payload
  Code___Build_Success_Payload --> Airtable___Save_Etsy_Draft
  Airtable___Save_Etsy_Draft --> Batch___Split_Records
  Airtable___Log_Etsy_Error --> Batch___Split_Records
```
