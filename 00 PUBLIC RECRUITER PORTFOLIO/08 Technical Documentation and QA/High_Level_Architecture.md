# High-Level Architecture

```mermaid
flowchart LR
  Test[Test] --> Classify[Classify Failure]
  Classify --> Fix[Fix Prompt or Logic]
  Fix --> Retest[Retest]
  Retest --> Doc[Document]
```
