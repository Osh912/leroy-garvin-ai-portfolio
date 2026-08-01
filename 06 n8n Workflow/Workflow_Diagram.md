# n8n Workflow — Workflow Diagram

## Generic Stage Sequencing Flow

```mermaid
flowchart TD
    A[Trigger] --> B[Stage Validation]
    B --> C{Required inputs present?}
    C -->|No| D[Stop / request needed data]
    C -->|Yes| E[Next-Step Action]
    E --> F[Status Update]
    F --> G{Review checkpoint needed?}
    G -->|Yes| H{Pass review?}
    G -->|No| I[Handoff to next stage]
    H -->|Yes| I
    H -->|No| J[Refine / retest path]
    J --> E
```

## Prompt-Assisted Review Flow

```mermaid
flowchart TD
    A[AI-assisted step complete] --> B[Capture output]
    B --> C[Validation check]
    C --> D{Complete and process-aligned?}
    D -->|Yes| E[Document result]
    E --> F[Continue to next stage]
    D -->|No| G[Issue note + refine prompt/logic]
    G --> H[Retest same path]
```

## Failure Logging Flow

```mermaid
flowchart TD
    A[Failure detected] --> B[Capture details]
    B --> C[Classify cause]
    C --> D[Update documentation]
    D --> E[Retest reminder]
```

## Related
- [Workflow_Templates.md](./Workflow_Templates.md)
- [Testing_and_QA.md](./Testing_and_QA.md)
- [Troubleshooting.md](./Troubleshooting.md)
