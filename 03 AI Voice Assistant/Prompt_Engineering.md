# AI Voice Assistant — Prompt Engineering

## Prompt Strategy Overview
Prompt engineering was used as an operational control method. Prompts were designed to enforce stage adherence, one-question-at-a-time behavior, confirmation checkpoints, and clear progression through the booking workflow.

## System / Role Instructions
Prompts were written to position the assistant as a professional booking guide for Right Outside Auto Detailing LLC. Instructions emphasized clarity, process control, and customer-friendly language without technical jargon.

## Key Prompt Patterns Used
- **Stage control** — Keep the assistant inside the current workflow stage
- **One-question-at-a-time** — Avoid stacking multiple questions in one turn
- **Confirmation checkpoints** — Require pricing and appointment confirmation before advancing
- **Anti-loop guidance** — Advance after valid answers instead of repeating the same question
- **Address handling** — Collect street address and ZIP separately; confirm service location
- **Order enforcement** — Vehicle/service → pricing → confirmation → customer details → address → appointment

## Example Scenarios Tested
- Complete booking with valid answers at each stage
- Pricing confirmation skipped or delayed
- Repeated questions after information already provided
- Assistant stuck in a loop
- Address or city recognition confusion
- Incorrect booking order
- Appointment confirmation before required details collected

## Iteration Process
1. Run scenario test
2. Record observed failure
3. Classify likely cause (prompt, logic, sequencing, business rule)
4. Refine prompt or conversation logic
5. Retest same scenario
6. Document change and outcome

## Guardrails & Edge Cases
- Incomplete answers
- Unclear vehicle details
- Location details that need explicit confirmation
- Attempts to skip pricing confirmation
- Workflow loops and repeated questions

## Lessons for Future Prompt Work
Prompt changes work best when tied to defined workflow stages and acceptance criteria. Broad wording changes without stage clarity often fail to fix sequencing problems.

**Related:** [Testing and QA](./Testing_and_QA.md) · [Challenges](./Challenges.md) · [Prompt Engineering Resume](../01%20Resume/Prompt_Engineering_Resume.md)
