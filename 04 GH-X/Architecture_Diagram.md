# GH-X — Architecture Diagram

## Layered Architecture

```mermaid
flowchart LR
    P[Process Layer<br/>stages, inputs, outputs, checkpoints]
    PR[Prompt Layer<br/>instructions, constraints, review points]
    A[Automation Layer<br/>n8n sequencing concepts]
    D[Data Layer<br/>Airtable status/records planning]
    Q[Quality Layer<br/>test, RCA, refine, document]

    P --> PR --> A --> D --> Q
    Q -->|Refine| PR
    Q -->|Refine| A
    Q -->|Refine| D
    Q -->|Refine| P
```

## Component View

```mermaid
flowchart TB
    subgraph Design["Design Inputs"]
        REQ[Process requirements]
        STAGE[Stage definitions]
    end

    subgraph Build["Build Concepts"]
        PROMPT[Prompt strategies]
        N8N[n8n workflow ideas]
        AT[Airtable structure plans]
    end

    subgraph Validate["Validate"]
        TEST[Structured testing]
        RCA[Root cause analysis]
        DOC[Process documentation]
    end

    REQ --> STAGE
    STAGE --> PROMPT
    STAGE --> N8N
    STAGE --> AT
    PROMPT --> TEST
    N8N --> TEST
    AT --> TEST
    TEST --> RCA --> DOC --> PROMPT
```

## Scope Note
Architecture documents concept-level AI Operations design. Tools are used at design/test/documentation depth already recorded in this portfolio.
