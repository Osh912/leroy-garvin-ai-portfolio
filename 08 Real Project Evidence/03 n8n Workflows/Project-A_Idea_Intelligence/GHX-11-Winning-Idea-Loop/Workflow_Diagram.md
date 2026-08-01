# Workflow Diagram — GHX-11-Winning-Idea-Loop

**Source:** `GHX-11-Winning-Idea-Loop.json` · **Status:** Functional Build · **Complexity:** Intermediate  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Weekly_Idea_Loop["Schedule · Weekly Idea Loop"]
  Airtable___Search_Top_Winners["Airtable · Search Top Winners"]
  Code___Build_Winner_Analysis["Code · Build Winner Analysis"]
  Filter___Has_Winners["Filter · Has Winners"]
  HTTP___OpenAI_Ideas["HTTP · OpenAI Ideas"]
  Code___Parse_New_Ideas["Code · Parse New Ideas"]
  Airtable___Create_Idea_Rows["Airtable · Create Idea Rows"]
  Code___Run_Complete["Code · Run Complete"]
  No_Op___No_Winners["No Op · No Winners"]
  Schedule___Weekly_Idea_Loop --> Airtable___Search_Top_Winners
  Airtable___Search_Top_Winners --> Code___Build_Winner_Analysis
  Code___Build_Winner_Analysis --> Filter___Has_Winners
  Filter___Has_Winners --> HTTP___OpenAI_Ideas
  Filter___Has_Winners --> No_Op___No_Winners
  HTTP___OpenAI_Ideas --> Code___Parse_New_Ideas
  Code___Parse_New_Ideas --> Airtable___Create_Idea_Rows
  Airtable___Create_Idea_Rows --> Code___Run_Complete
```
