# Interview Stories — Leroy Garvin Jr

## How to Use This Document
Use these STAR stories for AI Operations, AI Trainer, AI Quality Assurance, Prompt Engineering Support, Workflow Automation, and AI Data Annotation interviews. Keep answers concise: roughly 60–90 seconds spoken. Lead with the business context, focus on actions you personally took, and close with a truthful result without inventing metrics.

## Story Index
1. Solving a difficult problem — AI getting stuck in booking conversations
2. Finding and fixing workflow failures — loops, repeated questions, incorrect order
3. Improving an AI conversation through testing — iterative prompt refinement
4. Designing a workflow from scratch — AI voice booking assistant
5. Learning a new technology independently — n8n, Airtable, prompt systems
6. Managing multiple priorities — running the business while building AI workflows
7. Receiving feedback and improving a process — refining after observed failures
8. Working through uncertainty — designing automation concepts without a fixed blueprint
9. Improving customer experience — clearer booking flow and one-question-at-a-time design
10. Explaining a technical idea to a non-technical customer — making AI booking simple

---

## Story 1: Solving a Difficult Problem
**Interview prompt this answers:** “Tell me about a time you solved a difficult problem.”

### Situation
While designing the AI voice booking assistant for Right Outside Auto Detailing LLC in Savannah, Georgia, I found that the assistant could get stuck during customer conversations. Instead of moving cleanly through booking steps, it sometimes repeated itself, stalled, or failed to advance after a valid answer.

### Task
I needed to diagnose why the conversation was breaking down and redesign the workflow so the assistant could guide customers from service qualification to appointment confirmation without getting stuck.

### Action
I treated the issue like an operations problem. I mapped the intended conversation stages, tested full booking scenarios, and documented where the assistant stalled. Then I performed root cause analysis to determine whether the failure came from unclear prompts, missing business rules, weak stage transitions, or incorrect booking order. I refined the conversation logic, strengthened confirmation checkpoints, updated prompts to enforce one question at a time, and retested until the conversation could move forward more reliably.

### Result
I improved the assistant’s ability to progress through the booking workflow without getting stuck as often. The conversation logic became clearer, the prompts were more controlled, and I created documentation that made future troubleshooting easier. I did not claim production volume metrics; the improvement was in workflow reliability and conversation quality.

### Skills Demonstrated
Root cause analysis, AI workflow design, prompt refinement, structured testing, process documentation, problem solving

### Interview Tips
- Emphasize diagnosis before fixing.
- Say what you personally owned: design, testing, documentation, and iteration.
- Avoid inventing call volume or conversion numbers.

### Common Follow-Up Questions
- How did you know the root cause was the prompt versus the workflow logic?
- What did you change first, and why?
- How did you decide the fix was good enough to move forward?

---

## Story 2: Finding and Fixing Workflow Failures
**Interview prompt this answers:** “Describe a time you found and fixed a process failure.”

### Situation
During testing of the AI-assisted booking workflow for Right Outside Auto Detailing LLC, I discovered several workflow failures: repeated questions, conversation loops, incorrect booking order, pricing confirmation issues, and address handling problems.

### Task
My task was to identify the failures systematically, understand why they happened, and fix the workflow so customers could complete booking steps in the correct order.

### Action
I created test scenarios covering complete bookings and edge cases. For each failure, I recorded the expected behavior, the actual behavior, and the likely cause. For example, when the assistant asked questions out of order, I restructured the conversation stages. When it looped, I strengthened stage-transition instructions. When pricing confirmation failed, I updated business rules so pricing had to be confirmed before collecting customer details. I documented each issue, applied a targeted fix, and retested the same scenario.

### Result
The workflow became more consistent and easier to follow. Failures were reduced through structured testing and documentation, and I developed a repeatable method for classifying and fixing AI workflow issues.

### Skills Demonstrated
AI quality assurance, workflow optimization, issue tracking, root cause analysis, structured testing, continuous improvement

### Interview Tips
- Use one concrete failure example, then briefly mention that you applied the same method to others.
- Recruiters like hearing: observe → classify → fix → retest → document.

### Common Follow-Up Questions
- Which failure was hardest to fix?
- How do you prioritize which bugs to solve first?
- How do you prevent the same failure from returning?

---

## Story 3: Improving an AI Conversation Through Testing
**Interview prompt this answers:** “Tell me about a time you improved an AI system through testing.”

### Situation
The AI voice booking assistant for my detailing business needed to sound clear and follow a reliable booking sequence. Early versions could confuse the conversation by repeating questions, skipping steps, or handling addresses inconsistently.

### Task
I needed to improve the conversation quality through iterative testing and prompt refinement so the assistant asked one question at a time and collected the right information in the right order.

### Action
I ran repeated booking tests and evaluated each response against expected workflow behavior. When the assistant repeated questions, I refined prompts to check whether information had already been collected. When city recognition created confusion, I adjusted the logic to rely more on ZIP code and explicit address confirmation. When the assistant moved too quickly, I added confirmation checkpoints for pricing and appointment details. After each change, I retested the same scenario and documented what improved.

### Result
The conversation became clearer and more controlled. Prompt instructions were stronger, customer questions were less ambiguous, and the booking flow better matched the intended process. The improvement came from iterative evaluation, not from a one-time rewrite.

### Skills Demonstrated
Conversational AI testing, prompt engineering, iterative refinement, quality evaluation, customer experience optimization

### Interview Tips
- Walk through one before/after example without inventing metrics.
- Stress that you used testing evidence, not guesses, to guide changes.

### Common Follow-Up Questions
- How do you evaluate whether a prompt change actually helped?
- What test cases do you always include?
- How do you avoid over-constraining the assistant?

---

## Story 4: Designing a Workflow From Scratch
**Interview prompt this answers:** “Tell me about a time you designed a process or workflow from scratch.”

### Situation
As the owner of Right Outside Auto Detailing LLC, I needed a better way to handle customer booking conversations and reduce missed-call friction. There was no existing AI booking workflow for the business, so I had to design one from scratch.

### Task
I needed to design a complete AI-assisted voice booking workflow that could answer calls, qualify customers, provide pricing, collect booking details, offer appointment times, confirm appointments, and close professionally.

### Action
I analyzed the real booking process and mapped it into controlled stages: greeting, service qualification, vehicle identification, pricing, pricing confirmation, name collection, address and ZIP code collection, appointment options, appointment confirmation, and call closing. I wrote conversation logic, business rules, pricing logic, and prompt strategies. I also planned how tools such as ChatGPT, n8n, Twilio, and Airtable would support the workflow design and automation concepts. Then I tested the full flow and refined it based on observed failures.

### Result
I produced a structured booking workflow with clear stages, documented logic, and an iterative testing process. The design gave the business a controlled conversation framework instead of an unstructured call experience.

### Skills Demonstrated
AI workflow design, process mapping, business rule development, prompt strategy, end-to-end ownership

### Interview Tips
- Emphasize starting from the business process, not from the tool.
- Mention stage design and checkpoints; recruiters associate that with AI Operations maturity.

### Common Follow-Up Questions
- How did you decide the order of the stages?
- What would you redesign first if you started again?
- How did you handle incomplete customer answers?

---

## Story 5: Learning a New Technology Independently
**Interview prompt this answers:** “Tell me about a time you taught yourself a new tool or technology.”

### Situation
To support AI-assisted business automation for Right Outside Auto Detailing LLC and related workflow projects such as GH-X, I needed to learn no-code automation and AI workflow tools on my own. I did not have a formal training program assigned to me.

### Task
I needed to independently learn enough about tools such as n8n, Airtable, ChatGPT, and Claude to design workflow ideas, plan databases, create prompt strategies, test automation concepts, and document processes.

### Action
I learned by building. I started with small workflow ideas, studied how each tool handled stages and data, and practiced connecting process logic to automation concepts. For prompts, I used ChatGPT and Claude to prototype instructions, then tested and refined them. For n8n and Airtable, I designed workflow sequences and database planning structures that matched real process needs. When something failed, I documented the issue, researched the likely cause, adjusted the design, and retested.

### Result
I became able to independently design, test, and document AI automation workflow concepts using no-code tools and prompt engineering. More importantly, I developed a learning method based on experimentation, root cause analysis, and continuous improvement.

### Skills Demonstrated
Self-directed learning, no-code automation, prompt engineering, process documentation, continuous improvement

### Interview Tips
- Focus on how you learn: build, test, document, refine.
- Be honest that this was hands-on learning through projects, not a certification claim.

### Common Follow-Up Questions
- Which tool was hardest to learn and why?
- How do you stay current with AI tools?
- How do you know when you understand a tool well enough to use it in a workflow?

---

## Story 6: Managing Multiple Priorities
**Interview prompt this answers:** “Tell me about a time you managed multiple priorities.”

### Situation
While running Right Outside Auto Detailing LLC, I was also designing and testing AI-assisted workflows, including the voice booking assistant and GH-X automation concepts. That meant balancing customer service operations with AI workflow design, testing, and documentation.

### Task
I needed to keep the business operating while still making meaningful progress on AI workflow development without letting either side become disorganized.

### Action
I prioritized by business impact and process risk. Customer service and active booking needs came first. Then I scheduled focused blocks for AI workflow work: mapping conversation stages, testing prompts, documenting failures, and refining automation ideas. I broke larger AI projects into smaller tasks so I could make progress between business responsibilities. I also documented work in progress so I could resume testing and prompt refinement efficiently after interruptions.

### Result
I maintained ownership of both business operations and AI workflow development. Progress continued through structured prioritization and documentation rather than trying to finish everything at once.

### Skills Demonstrated
Prioritization, time management, operational ownership, process discipline, self-management

### Interview Tips
- Recruiters want to hear decision criteria: urgency, customer impact, and process risk.
- Avoid sounding scattered; show a method.

### Common Follow-Up Questions
- How do you decide what to postpone?
- What happens when a customer need interrupts technical work?
- How do you track unfinished workflow tasks?

---

## Story 7: Receiving Feedback and Improving a Process
**Interview prompt this answers:** “Tell me about a time you received feedback and improved because of it.”

### Situation
During AI workflow testing for the voice booking assistant, the feedback often came from observed system behavior rather than a manager. The assistant’s failures—repeated questions, stuck conversations, incorrect order, and pricing confirmation issues—were clear signals that the process needed improvement.

### Task
I needed to treat those test results as feedback, improve the process, and verify that the changes actually made the workflow stronger.

### Action
I recorded each failure as actionable feedback. Instead of making broad, unfocused changes, I identified the specific breakdown, adjusted the related prompt or business rule, and retested. For example, feedback from pricing confirmation failures led me to require explicit pricing confirmation before moving into customer data collection. Feedback from address issues led me to separate address and ZIP code collection and confirm location details more clearly. I documented the feedback, the change, and the retest outcome.

### Result
The booking process became more controlled and easier to evaluate. I also strengthened my habit of converting feedback into documented process improvements rather than temporary patchwork.

### Skills Demonstrated
Openness to feedback, process improvement, AI quality assurance, documentation, iterative learning

### Interview Tips
- If asked about manager feedback, be honest that much of your feedback came from structured testing and customer-experience observation.
- Show that you welcome corrective signals and act on them systematically.

### Common Follow-Up Questions
- How do you separate useful feedback from noise?
- Have you ever disagreed with feedback? What did you do?
- How do you confirm an improvement actually worked?

---

## Story 8: Working Through Uncertainty
**Interview prompt this answers:** “Tell me about a time you worked through ambiguity or uncertainty.”

### Situation
When I started designing AI automation concepts for GH-X and AI-assisted booking workflows for my business, there was no complete blueprint. I had to figure out which stages mattered, how prompts should control behavior, how n8n and Airtable should support the process, and how to test reliability without a predefined playbook.

### Task
I needed to move forward productively despite uncertainty and create a workable workflow design through experimentation and structured learning.

### Action
I reduced uncertainty by defining what “good” looked like for each stage: required inputs, expected outputs, and quality checks. I built small workflow ideas first, tested them, and used failures to guide the next design decision. When I was unsure whether a problem was caused by prompt wording or workflow sequencing, I isolated variables, changed one part at a time, and documented the result. I also created process notes so future decisions were based on evidence instead of memory.

### Result
I turned an unclear automation concept into a structured workflow design approach with clearer stages, stronger prompts, and a repeatable testing method. Uncertainty did not stop progress because I used iteration and documentation as control systems.

### Skills Demonstrated
Ambiguity tolerance, analytical thinking, experimental design, root cause analysis, continuous learning

### Interview Tips
- Show that you create structure when none exists.
- Mention isolating variables; that sounds highly operational and recruiter-friendly.

### Common Follow-Up Questions
- What did you do when two possible solutions seemed equally likely?
- How do you avoid overbuilding when requirements are unclear?
- What documentation helped you most?

---

## Story 9: Improving Customer Experience
**Interview prompt this answers:** “Tell me about a time you improved the customer experience.”

### Situation
For Right Outside Auto Detailing LLC, missed calls and unstructured booking conversations created a weaker customer experience. Customers needed a clear path to understand services, pricing, and appointment details.

### Task
I needed to design an AI-assisted booking conversation that felt clearer, more professional, and easier for customers to complete.

### Action
I redesigned the experience around customer clarity. The assistant was built to ask one question at a time, confirm pricing before continuing, collect name and service location details carefully, offer appointment times, and end the call professionally. I tested the conversation for friction points such as repeated questions, confusing address handling, and skipped confirmations. Then I refined prompts and workflow stages to reduce those pain points.

### Result
The booking conversation became more structured and customer-friendly. Customers could be guided through a clearer sequence, and I improved the process by focusing on comprehension, confirmation, and professional closure rather than rushing through questions.

### Skills Demonstrated
Customer experience optimization, conversational design, process thinking, quality testing, service operations

### Interview Tips
- Connect technical work to customer clarity.
- Stay truthful: talk about improved structure and reduced friction, not unverified revenue or satisfaction scores.

### Common Follow-Up Questions
- How do you measure customer experience without formal survey data?
- What customer friction point mattered most?
- How do you balance automation speed with clarity?

---

## Story 10: Explaining a Technical Idea to a Non-Technical Customer
**Interview prompt this answers:** “Tell me about a time you explained something technical to a non-technical person.”

### Situation
As I developed AI-assisted booking and automation workflows for Right Outside Auto Detailing LLC, I needed to explain the concept in plain language—especially to customers or contacts who were not familiar with AI tools, prompts, n8n, or Airtable.

### Task
I needed to explain how an AI voice booking assistant could help with calls and appointments without using technical jargon that would confuse a non-technical listener.

### Action
I translated the system into customer outcomes. Instead of talking about prompt engineering or workflow nodes, I explained that the assistant is designed to answer the call, ask simple questions one at a time, confirm the vehicle and services, share pricing, collect the address, offer appointment times, and confirm the booking. If someone asked how it works, I compared it to a guided checklist: the AI follows a clear order, confirms important details, and helps make sure nothing important is skipped. I avoided tool-heavy language unless the person asked for it.

### Result
I could explain the AI booking idea in a way that was easy to understand and focused on customer value. This strengthened my ability to communicate technical workflow concepts clearly—an important skill for AI Operations and cross-functional work.

### Skills Demonstrated
Clear communication, customer empathy, technical translation, stakeholder communication, customer experience thinking

### Interview Tips
- Show the exact plain-language explanation you would use.
- Recruiters listen for whether you can stay non-technical without becoming vague.

### Common Follow-Up Questions
- How do you handle someone who is skeptical of AI?
- How would you explain a workflow failure to a non-technical teammate?
- How do you decide how much detail to share?

---

## Quick Prep Notes for Recruiters’ Favorite Themes
- Always name the business context: Right Outside Auto Detailing LLC.
- Always name your ownership: you designed, tested, documented, and improved the workflows yourself.
- Always keep results qualitative unless you later verify a real metric.
- Always connect stories to target roles: AI Operations, AI Trainer, AI QA, Prompt Engineering Support, Workflow Automation, AI Data Annotation.

## Practice Order Before Interviews
1. Story 4 — Designing a workflow from scratch
2. Story 2 — Finding and fixing workflow failures
3. Story 3 — Improving an AI conversation through testing
4. Story 1 — Solving a difficult problem
5. Story 9 — Improving customer experience
6. Remaining stories as backup for common behavioral questions
