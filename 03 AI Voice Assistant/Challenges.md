# AI Voice Assistant — Challenges

## Challenge Overview
The main challenge was designing a conversational AI workflow that could guide customers through a multi-step booking process without getting stuck, repeating questions, skipping steps, or collecting incomplete information.

## Challenge 1 — AI Getting Stuck in Conversations
### What Happened
The assistant sometimes stalled instead of advancing after a valid customer answer.
### Why It Mattered
Stalled conversations create customer frustration and break the booking process.
### How It Was Handled
Mapped stages, identified weak transition prompts, refined stage-boundary instructions, and retested until progression improved.

## Challenge 2 — Repeated Questions and Workflow Loops
### What Happened
The assistant repeated questions or looped on the same stage.
### Why It Mattered
Repeated questions reduce trust and make the conversation harder to complete.
### How It Was Handled
Added anti-loop prompt logic, confirmed whether required information was already collected, and strengthened advance-only-after-confirmation rules.

## Challenge 3 — Pricing Confirmation and Booking Order
### What Happened
The assistant sometimes moved forward before pricing was confirmed or collected details out of order.
### Why It Mattered
Pricing and sequencing errors create operational risk and incomplete bookings.
### How It Was Handled
Strengthened business rules, enforced fixed stage order, and required explicit pricing confirmation before customer data collection.

## Challenge 4 — Address and Location Handling
### What Happened
Address handling and city recognition created confusion during booking.
### Why It Mattered
Service location is required for mobile detailing operations.
### How It Was Handled
Separated address and ZIP collection, relied more on explicit confirmation, and refined location-related prompt instructions.

## Takeaways
Most failures required distinguishing prompt issues from workflow sequencing and business-rule gaps. Structured testing and documentation made improvements repeatable.

## Root Cause Analysis Reference
A consolidated failure → cause → fix table is maintained in [Testing and QA](./Testing_and_QA.md). Challenge narratives above map to those documented cause buckets: prompt ambiguity, weak stage boundaries, missing business rules, incorrect sequencing, and incomplete confirmation logic.

**Related:** [Testing and QA](./Testing_and_QA.md) · [Improvements](./Improvements.md) · [Outcome](./Outcome.md)
