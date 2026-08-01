# Airtable — Workflow Diagram

## Structure Design and Validation Workflow

```mermaid
flowchart TD
    A[Map real workflow stages] --> B[Define tables and fields]
    B --> C[Add status and confirmation checkpoints]
    C --> D[Separate issue-logging table]
    D --> E[Plan n8n automation touchpoints]
    E --> F[Walk scenarios against structure]
    F --> G{Gaps found?}
    G -->|Yes| H[Adjust fields/statuses]
    H --> I[Document change]
    I --> F
    G -->|No| J[Keep structure as reviewable plan]
```

## Booking Record Lifecycle (Conceptual)

```mermaid
flowchart TD
    A[New booking request record] --> B[Update workflow stage]
    B --> C{Pricing confirmed?}
    C -->|No| D[Remain in pricing stage]
    C -->|Yes| E[Collect/store name + address + ZIP]
    E --> F{Appointment confirmed?}
    F -->|No| G[Appointment options pending]
    F -->|Yes| H[Stage complete / review notes]
    H --> I{QA issue found?}
    I -->|Yes| J[Create Workflow Issues record]
    I -->|No| K[Ready for handoff / archive notes]
```

## Related
- [Database_Structure.md](./Database_Structure.md)
- [Automation_Planning.md](./Automation_Planning.md)
- [Testing_and_QA.md](./Testing_and_QA.md)
