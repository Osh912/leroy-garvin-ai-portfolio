# GH-X — Workflow Diagram

## Design-to-Improvement Workflow

```mermaid
flowchart TD
    A[Define Process Stages] --> B[Design Prompt Layer]
    B --> C[Plan Automation Layer - n8n]
    C --> D[Plan Data Layer - Airtable]
    D --> E[Run Quality Layer - Test]
    E --> F{Meets Expected Behavior?}
    F -->|No| G[Root Cause Analysis]
    G --> H{Cause Type?}
    H -->|Prompt Issue| B
    H -->|Sequencing Issue| C
    H -->|Data / Status Gap| D
    H -->|Documentation Gap| I[Update Process Documentation]
    I --> E
    F -->|Yes| J[Document and Continue Continuous Improvement]
```

## Automation Logic Pattern (Per Stage)

```mermaid
flowchart LR
    T[Trigger] --> I[Input]
    I --> A[Action / AI-assisted step]
    A --> V[Validation]
    V -->|Pass| H[Handoff]
    V -->|Fail| R[Refine prompt or logic]
    R --> A
```

## Related
- [Workflow_Design.md](./Workflow_Design.md)
- [AI_Automation.md](./AI_Automation.md)
- [Testing_and_QA.md](./Testing_and_QA.md)
