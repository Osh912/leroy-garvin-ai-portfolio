# Workflow Diagram — GH-X OpenAI Image Generator

**Source:** `GH-X OpenAI Image Generator.json` · **Status:** Functional Build · **Complexity:** Intermediate  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Cover_Image_Run["Schedule · Cover Image Run"]
  Airtable___Search_One_Ready_To_Design["Airtable · Search One Ready To Design"]
  Code___Build_OpenAI_Image_Body["Code · Build OpenAI Image Body"]
  HTTP___OpenAI_Images["HTTP · OpenAI Images"]
  Code___Response_To_Binary["Code · Response To Binary"]
  Filter___Image_OK["Filter · Image OK"]
  Google_Drive___Upload_Cover["Google Drive · Upload Cover"]
  Code___Merge_Drive_URL["Code · Merge Drive URL"]
  Airtable___Update_By_Record_Id["Airtable · Update By Record Id"]
  Airtable___Log_Error["Airtable · Log Error"]
  Schedule___Cover_Image_Run --> Airtable___Search_One_Ready_To_Design
  Airtable___Search_One_Ready_To_Design --> Code___Build_OpenAI_Image_Body
  Code___Build_OpenAI_Image_Body --> HTTP___OpenAI_Images
  HTTP___OpenAI_Images --> Code___Response_To_Binary
  Code___Response_To_Binary --> Filter___Image_OK
  Filter___Image_OK --> Google_Drive___Upload_Cover
  Filter___Image_OK --> Airtable___Log_Error
  Google_Drive___Upload_Cover --> Code___Merge_Drive_URL
  Code___Merge_Drive_URL --> Airtable___Update_By_Record_Id
```
