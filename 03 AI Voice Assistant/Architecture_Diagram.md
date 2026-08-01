# AI Voice Booking Assistant — Architecture Diagram

## Architecture Overview
The assistant is treated as an operational workflow with process control, prompt control, optional no-code support concepts, and a quality loop.

```mermaid
flowchart TB
    subgraph Customer["Customer Channel"]
        CALL[Incoming Call]
    end

    subgraph Conversation["Conversation Control Layer"]
        LOGIC[Conversation Logic]
        RULES[Business Rules + Pricing Logic]
        PROMPTS[Prompt Engineering Controls]
    end

    subgraph Stages["Booking Stage Layer"]
        S1[Greeting]
        S2[Service + Vehicle]
        S3[Pricing + Confirm]
        S4[Name + Address/ZIP]
        S5[Appointment + Confirm]
        S6[Professional Close]
    end

    subgraph Support["Supporting Concepts"]
        N8N[n8n sequencing concepts]
        AT[Airtable organization concepts]
        TW[Twilio in voice technology set]
    end

    subgraph Quality["Quality Layer"]
        TEST[Scenario Testing]
        RCA[Root Cause Analysis]
        DOC[Process Documentation]
        CI[Continuous Improvement]
    end

    CALL --> LOGIC
    LOGIC --> RULES
    RULES --> PROMPTS
    PROMPTS --> S1 --> S2 --> S3 --> S4 --> S5 --> S6
    S1 -.-> TEST
    S3 -.-> TEST
    S5 -.-> TEST
    TEST --> RCA --> DOC --> CI --> PROMPTS
    N8N -.-> LOGIC
    AT -.-> S4
    TW -.-> CALL
```

## Layer Descriptions
| Layer | Responsibility |
|-------|----------------|
| Conversation Control | Logic, business rules, pricing rules, prompts |
| Booking Stages | Ordered customer information collection and confirmations |
| Supporting Concepts | n8n / Airtable / Twilio at documented scope only |
| Quality | Test → classify → fix → retest → document |

## Scope Note
Architecture reflects design/testing documentation. Supporting tools are shown at concept/technology-set depth already recorded in this portfolio.
