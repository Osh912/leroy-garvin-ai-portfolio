# n8n Workflow — Architecture Diagram

## Automation Architecture

```mermaid
flowchart TB
    subgraph Triggers["Triggers"]
        T1[New process record / stage-ready]
        T2[AI-assisted step complete]
        T3[Failed test / weak transition]
    end

    subgraph Core["n8n Concept Core"]
        V[Validate inputs / prior stage]
        A[Execute next-step action]
        R[Review checkpoint]
        S[Status / documentation update]
    end

    subgraph Branches["Outcomes"]
        H[Handoff to next stage]
        F[Refine prompt or logic]
        L[Failure log + retest reminder]
    end

    subgraph Related["Related Systems"]
        AT[Airtable status concepts]
        AI[ChatGPT / Claude prompt-assisted steps]
        DOC[Process documentation]
    end

    T1 --> V --> A --> R
    T2 --> V
    T3 --> L
    R -->|Pass| S --> H
    R -->|Fail| F --> A
    L --> DOC
    S --> AT
    A -.-> AI
```

## Template Architecture Map
| Template | Primary Path |
|----------|--------------|
| Stage Sequencing | Trigger → Validate → Action → Status → Review → Handoff |
| Prompt-Assisted Review | AI complete → Capture → Validate → Review branch → Continue/Refine |
| Failure Logging | Failure → Capture → Classify → Document → Retest reminder |

## Scope Note
Architecture reflects designed/tested workflow concepts supporting Voice Assistant and GH-X work.
