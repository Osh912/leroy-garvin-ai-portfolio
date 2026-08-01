# Workflow Diagram — GHX-09-Self-Healing-QA

**Source:** `GHX-09-Self-Healing-QA.json` · **Status:** Functional Build · **Complexity:** Intermediate  
**Execution evidence:** Not found — definition only.

```mermaid
flowchart TD
  Schedule___QA_Sweep["Schedule · QA Sweep"]
  Airtable___Search_Failed_Rows["Airtable · Search Failed Rows"]
  Batch___Split_Records["Batch · Split Records"]
  Code___Classify_Failure["Code · Classify Failure"]
  Filter___Can_Auto_Retry["Filter · Can Auto Retry"]
  Airtable___Requeue_For_Retry["Airtable · Requeue For Retry"]
  Airtable___Flag_Manual_Review["Airtable · Flag Manual Review"]
  Filter___Webhook_Set["Filter · Webhook Set"]
  HTTP___Admin_Alert["HTTP · Admin Alert"]
  No_Op___Skip_Alert["No Op · Skip Alert"]
  Code___Batch_Complete["Code · Batch Complete"]
  Schedule___QA_Sweep --> Airtable___Search_Failed_Rows
  Airtable___Search_Failed_Rows --> Batch___Split_Records
  Batch___Split_Records --> Code___Classify_Failure
  Batch___Split_Records --> Code___Batch_Complete
  Code___Classify_Failure --> Filter___Can_Auto_Retry
  Filter___Can_Auto_Retry --> Airtable___Requeue_For_Retry
  Filter___Can_Auto_Retry --> Airtable___Flag_Manual_Review
  Airtable___Requeue_For_Retry --> Filter___Webhook_Set
  Airtable___Flag_Manual_Review --> Filter___Webhook_Set
  Filter___Webhook_Set --> HTTP___Admin_Alert
  Filter___Webhook_Set --> No_Op___Skip_Alert
  HTTP___Admin_Alert --> Batch___Split_Records
  No_Op___Skip_Alert --> Batch___Split_Records
```
