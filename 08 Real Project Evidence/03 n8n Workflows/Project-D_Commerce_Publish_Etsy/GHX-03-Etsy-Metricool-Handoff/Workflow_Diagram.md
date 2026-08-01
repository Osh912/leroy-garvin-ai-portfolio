# Workflow Diagram — GHX-03-Etsy-Metricool-Handoff

**Source:** `GHX-03-Etsy-Metricool-Handoff.json` · **Status:** Functional Build · **Complexity:** Beginner  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___Publishing_Prep["Schedule · Publishing Prep"]
  Airtable___Search_Ready_Rows["Airtable · Search Ready Rows"]
  Code___Build_Draft_JSON["Code · Build Draft JSON"]
  Airtable___Save_Drafts["Airtable · Save Drafts"]
  Schedule___Publishing_Prep --> Airtable___Search_Ready_Rows
  Airtable___Search_Ready_Rows --> Code___Build_Draft_JSON
  Code___Build_Draft_JSON --> Airtable___Save_Drafts
```
