# High-Level Architecture

```mermaid
flowchart LR
  Trigger[Trigger] --> Validate[Validate Queue Item]
  Validate --> AI[Optional AI or API Step]
  AI --> Branch[Quality or Status Branch]
  Branch --> Write[Write Status to Airtable]
```
