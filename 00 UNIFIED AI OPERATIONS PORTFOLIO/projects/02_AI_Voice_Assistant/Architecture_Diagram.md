# Architecture Diagram — AI Voice Booking Assistant

```mermaid
flowchart TD
  Call[Customer Call] --> Logic[Staged Conversation Logic]
  Logic --> Rules[Business Rules and Pricing Gate]
  Rules --> Collect[Collect Details]
  Collect --> Book[Confirm Appointment]
  Book --> Close[Close]
  Logic --> QA[Test Classify Fix Retest]
```

Abstracted for public safety. Detailed private diagrams may exist in Private Master / prior evidence folders.
