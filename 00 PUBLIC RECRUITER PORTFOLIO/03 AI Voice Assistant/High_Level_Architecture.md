# High-Level Architecture (Public)

```mermaid
flowchart TD
  Call[Inbound Call] --> Stage[Staged Conversation Logic]
  Stage --> Rules[Business Rules and Pricing Gate]
  Rules --> Collect[Collect Customer and Location Details]
  Collect --> Appt[Offer and Confirm Appointment]
  Appt --> Close[Professional Close]
  Stage --> QA[Test Classify Fix Retest]
```
