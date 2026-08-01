# Workflow Diagram — Design + Reel Prompt Generator

**Source:** `Design + Reel Prompt Generator.json` · **Status:** Functional Build · **Complexity:** Intermediate  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule_Trigger["Schedule Trigger"]
  Search_records["Search records"]
  Loop_Over_Items["Loop Over Items"]
  Batch_complete["Batch complete"]
  Code_in_JavaScript["Code in JavaScript"]
  Update_record["Update record"]
  Schedule_Trigger --> Search_records
  Search_records --> Loop_Over_Items
  Loop_Over_Items --> Code_in_JavaScript
  Loop_Over_Items --> Batch_complete
  Code_in_JavaScript --> Update_record
  Update_record --> Loop_Over_Items
```
