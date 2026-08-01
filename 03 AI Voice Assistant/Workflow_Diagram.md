# AI Voice Booking Assistant — Workflow Diagram

## End-to-End Booking Workflow

```mermaid
flowchart TD
    A[Greeting / Call Intake] --> B[Service Qualification]
    B --> C[Vehicle Identification]
    C --> D[Pricing]
    D --> E{Pricing Confirmed?}
    E -->|No| D
    E -->|Yes| F[Collect Customer Name]
    F --> G[Collect Service Address + ZIP]
    G --> H{Location Confirmed?}
    H -->|No| G
    H -->|Yes| I[Offer Appointment Options]
    I --> J{Appointment Confirmed?}
    J -->|No| I
    J -->|Yes| K[Professional Close]
```

## Design Controls (Documented)
- One question at a time
- Pricing confirmed before customer data collection continues
- Address and ZIP collected with explicit confirmation
- Fixed stage order to reduce skipped steps and incorrect booking order
- Anti-loop / anti-repeat prompt refinements after testing

## Related
- [Workflow_Design.md](./Workflow_Design.md)
- [Testing_and_QA.md](./Testing_and_QA.md)
- [Architecture_Diagram.md](./Architecture_Diagram.md)
