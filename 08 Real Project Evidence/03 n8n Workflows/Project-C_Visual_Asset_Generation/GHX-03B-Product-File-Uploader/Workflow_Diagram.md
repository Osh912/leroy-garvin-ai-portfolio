# Workflow Diagram — GHX-03B-Product-File-Uploader

**Source:** `GHX-03B-Product-File-Uploader.json` · **Status:** Functional Build · **Complexity:** Advanced  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Product_File_Run["Schedule · Product File Run"]
  Set___Load_Product_Gen_Config["Set · Load Product Gen Config"]
  Code___Setup_Config["Code · Setup Config"]
  Airtable___Search_Needs_Product_File["Airtable · Search Needs Product File"]
  Batch___Split_Records["Batch · Split Records"]
  Code___Prepare_Product_Job["Code · Prepare Product Job"]
  Filter___Job_OK["Filter · Job OK"]
  HTTP___OpenAI_Product_Blueprint["HTTP · OpenAI Product Blueprint"]
  Code___Parse_Product_Blueprint["Code · Parse Product Blueprint"]
  Filter___Blueprint_OK["Filter · Blueprint OK"]
  Switch___Output_Format["Switch · Output Format"]
  Code___Generate_Product_File___PDF["Code · Generate Product File · PDF"]
  HTTP___OpenAI_Product_Image["HTTP · OpenAI Product Image"]
  Code___Image_To_Binary["Code · Image To Binary"]
  Filter___Image_OK["Filter · Image OK"]
  Code___Generate_Product_File___Visual["Code · Generate Product File · Visual"]
  Filter___Product_Binary_OK["Filter · Product Binary OK"]
  Google_Drive___Upload_Product_File["Google Drive · Upload Product File"]
  Code___Build_Download_URL["Code · Build Download URL"]
  Airtable___Write_Product_File_URL["Airtable · Write Product File URL"]
  Airtable___Log_File_Error["Airtable · Log File Error"]
  Code___Batch_Complete["Code · Batch Complete"]
  Schedule___Product_File_Run --> Set___Load_Product_Gen_Config
  Set___Load_Product_Gen_Config --> Code___Setup_Config
  Code___Setup_Config --> Airtable___Search_Needs_Product_File
  Airtable___Search_Needs_Product_File --> Batch___Split_Records
  Batch___Split_Records --> Code___Prepare_Product_Job
  Batch___Split_Records --> Code___Batch_Complete
  Code___Prepare_Product_Job --> Filter___Job_OK
  Filter___Job_OK --> HTTP___OpenAI_Product_Blueprint
  Filter___Job_OK --> Airtable___Log_File_Error
  HTTP___OpenAI_Product_Blueprint --> Code___Parse_Product_Blueprint
  Code___Parse_Product_Blueprint --> Filter___Blueprint_OK
  Filter___Blueprint_OK --> Switch___Output_Format
  Filter___Blueprint_OK --> Airtable___Log_File_Error
  Switch___Output_Format --> Code___Generate_Product_File___PDF
  Switch___Output_Format --> HTTP___OpenAI_Product_Image
  Switch___Output_Format --> HTTP___OpenAI_Product_Image
  Switch___Output_Format --> Airtable___Log_File_Error
  Code___Generate_Product_File___PDF --> Filter___Product_Binary_OK
  HTTP___OpenAI_Product_Image --> Code___Image_To_Binary
  Code___Image_To_Binary --> Filter___Image_OK
  Filter___Image_OK --> Code___Generate_Product_File___Visual
  Filter___Image_OK --> Airtable___Log_File_Error
  Code___Generate_Product_File___Visual --> Filter___Product_Binary_OK
  Filter___Product_Binary_OK --> Google_Drive___Upload_Product_File
  Filter___Product_Binary_OK --> Airtable___Log_File_Error
  Google_Drive___Upload_Product_File --> Code___Build_Download_URL
  Code___Build_Download_URL --> Airtable___Write_Product_File_URL
  Airtable___Write_Product_File_URL --> Batch___Split_Records
  Airtable___Log_File_Error --> Batch___Split_Records
```
