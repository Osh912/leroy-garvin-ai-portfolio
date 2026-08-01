# Workflow Diagram — GHX-01-Idea-Intelligence

**Source:** `GHX-01-Idea-Intelligence.json` · **Status:** Functional Build · **Complexity:** Beginner  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Weekly_Ideas["Schedule · Weekly Ideas"]
  Code___Build_OpenAI_Body["Code · Build OpenAI Body"]
  HTTP___OpenAI_Chat["HTTP · OpenAI Chat"]
  Code___Parse_Ideas["Code · Parse Ideas"]
  Airtable___Create_Product["Airtable · Create Product"]
  Schedule___Weekly_Ideas --> Code___Build_OpenAI_Body
  Code___Build_OpenAI_Body --> HTTP___OpenAI_Chat
  HTTP___OpenAI_Chat --> Code___Parse_Ideas
  Code___Parse_Ideas --> Airtable___Create_Product
```
