# AI Voice Assistant — Business Problem

## Problem Statement
Right Outside Auto Detailing LLC in Savannah, Georgia depends on timely customer conversations to explain services, provide pricing, collect booking details, and schedule appointments. Missed calls and unstructured booking conversations create operational risk: incomplete customer information, unclear service requests, pricing confusion, and appointments that cannot be confirmed confidently.

## Who Is Affected
- Customers calling to request mobile auto-detailing services
- The business owner responsible for scheduling and service delivery
- The booking process itself, when required details are skipped or collected out of order

## Current State (Before)
Before the AI-assisted workflow was designed, booking conversations could be inconsistent. Important details such as vehicle type, requested services, pricing confirmation, service address, ZIP code, and appointment time were not always collected in a controlled sequence. Missed calls added friction for customers trying to book a service.

## Desired State (After)
The business needed a voice booking workflow that could:
- Answer incoming calls
- Ask one question at a time
- Identify the customer's vehicle
- Determine requested services
- Calculate and confirm pricing before continuing
- Collect the customer's name, service address, and ZIP code
- Offer available appointment times
- Confirm the appointment
- End the call professionally

## Constraints
- Workflow had to remain understandable for non-technical customers
- Prompt and logic design needed to reduce loops, repeated questions, and skipped steps
- Address and location details required careful handling
- Pricing had to be confirmed before moving into customer data collection
- Tools used in the workflow design included ChatGPT, n8n, Twilio, and Airtable concepts

## Success Criteria (Qualitative Only)
- Assistant follows the intended booking sequence more consistently
- Common failure patterns are identified, documented, and reduced through testing
- Customer conversations become clearer and easier to evaluate
- Workflow documentation supports ongoing QA and process improvement

These criteria are qualitative process measures. No call volume, conversion rate, revenue, or deployment-scale metrics are claimed.

## Why This Matters
A controlled booking workflow improves customer experience and makes AI-assisted service operations easier to test, document, and improve. This project demonstrates practical AI Operations work: workflow design, prompt engineering, conversational AI testing, and quality assurance in a real business context.

**Related:** [Project Overview](./Project_Overview.md) · [Workflow Design](./Workflow_Design.md) · [Testing and QA](./Testing_and_QA.md)
