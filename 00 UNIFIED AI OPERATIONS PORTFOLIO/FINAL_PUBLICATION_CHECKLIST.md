# FINAL PUBLICATION CHECKLIST — GitHub & LinkedIn

**Status:** Do **not** publish until blockers below are checked.  
**Audit companion:** [FINAL_RECRUITER_AUDIT.md](./FINAL_RECRUITER_AUDIT.md)  
**Date:** 2026-07-20

---

## A. Best order for recruiters to review (recommended)

Send this order in your outreach / LinkedIn About / GitHub README “Start here”:

1. **Resume** — `01 Resume/FINAL_MASTER_RESUME.md`  
2. **GH-X Automation System** — end-to-end AI Ops story (strongest artifact-backed project)  
3. **AI Voice Booking Assistant** — business-owned conversational AI + QA story  
4. **Airtable Systems** — queue/data layer that makes automation explainable  
5. **n8n Capability** — how orchestration works (no downloadable JSON)  
6. **Technical Documentation & QA** — how you test and improve systems  
7. **About & Contact** — phone, email, LinkedIn  
8. **Legal / Usage Notice** — what is withheld and why  

Optional later: Cursor documentation evidence.  
**Never** lead with ServiceFlowAI or Private Master.

---

## B. GitHub publication checklist

### B1. What to publish
- [ ] Create a **new** public repo (or empty repo) dedicated to the recruiter pack  
- [ ] Upload / push **only** the contents of `00 PUBLIC RECRUITER PORTFOLIO/`  
- [ ] Root README of the repo = Public portfolio `README.md` (or thin wrapper pointing to it)  
- [ ] Include `.gitignore` that blocks `*.json`, `.env*`, `*credential*`, private paths

### B2. What must NEVER be published
- [ ] `00 PRIVATE MASTER PORTFOLIO/` (entire tree)  
- [ ] Any `*.json` workflow export  
- [ ] Airtable base/table/field IDs, PATs, API keys, tokens  
- [ ] Webhook URLs, n8n URLs with secrets  
- [ ] ServiceFlowAI source / `.env`  
- [ ] Unredacted screenshots (phone numbers, emails of customers, tokens in UI)  
- [ ] Desktop `~/Desktop/GH-X/workflows/` originals  
- [ ] Unified `_meta` / internal analysis JSON (now under Private Audit Reports)

### B3. Evidence gate (required before first push)
| ID | Item | Done? |
|----|------|-------|
| GHX-01 | System overview screenshot (sanitized) | [ ] |
| GHX-02 | Pipeline / architecture visual (sanitized) | [ ] |
| N8-01 | One n8n canvas (prefer complex workflow) | [ ] |
| N8-02 | Key nodes readable | [ ] |
| N8-03 | Node config with secrets cropped | [ ] |
| N8-04 | Execution history (empty state OK if honest) | [ ] |
| AT-01 | Airtable base overview sanitized | [ ] |
| AT-02 | Products (or key table) structure sanitized | [ ] |
| VA-01 | Voice booking stage map / flow visual | [ ] |
| VA-02 | Test-case sample (no customer PII) | [ ] |

- [ ] Update `09 Sanitized Screenshots/SCREENSHOT_EVIDENCE_TRACKER.md` only when files exist  
- [ ] Re-scan Public for secrets after adding images  
- [ ] Confirm Public `*.json` count still **0**

### B4. Claim gate
- [ ] No “Production Ready” unless execution evidence exists  
- [ ] No revenue, ROI, call volume, or customer-count claims  
- [ ] Status labels match audit: Functional Build / Evidence Pending where true  
- [ ] Employment start date remains honest (“not provided” / Present)  

### B5. Final GitHub pre-flight
- [ ] `find` Public for `.json` / `.env` → none  
- [ ] Open every Public README on phone-width — readable without jargon overload  
- [ ] Legal notice present  
- [ ] Contact block matches LinkedIn  
- [ ] **Then** push (user-initiated only)

---

## C. LinkedIn publication checklist

### C1. Profile text
- [ ] Headline matches target:  
  `AI Operations Specialist | Workflow Automation | Prompt Engineering | AI Testing & QA | Owner, Right Outside Auto Detailing LLC`  
  *(confirm exact “AI Testing & QA” wording before publish — Needs Review if you prefer alternate)*  
- [ ] About section: 3–5 lines on AI Ops + owned business; **no** metrics you cannot prove  
- [ ] Experience: Right Outside Auto Detailing LLC — Owner & AI Operations Specialist; start date only if verified  
- [ ] Featured: link to **GitHub public portfolio** (after GitHub is live)  
- [ ] Contact: same email/phone as portfolio (or LinkedIn message preference)

### C2. What to feature (order)
1. GitHub public portfolio link  
2. One-line GH-X summary (Functional Build / multi-stage automation)  
3. One-line Voice Assistant summary (conversational AI testing + booking workflow)  
4. Resume PDF only if sanitized and dated  

### C3. What not to post on LinkedIn
- [ ] Screenshots showing API keys, webhooks, customer names/phones  
- [ ] “Download my n8n workflows”  
- [ ] ServiceFlowAI proprietary details  
- [ ] Claims of production scale without evidence  

### C4. Soft launch sequence
1. Finish Evidence gate (B3)  
2. Publish GitHub Public pack  
3. Update LinkedIn Featured + About with GitHub URL  
4. Optional: one post describing **problem → your role → solution → status (Functional Build)** for GH-X or Voice — no invented results  

---

## D. Recruiter-facing one-pager (copy/paste when ready)

**Leroy Garvin Jr** — Savannah, Georgia, USA · Open to remote AI Operations roles  
I design and test AI-assisted operations: n8n + Airtable automation for digital product workflows (GH-X), and a conversational AI booking assistant for my detailing business, with structured QA and documentation.  
**Status:** Functional builds with definition-level and schema evidence; production metrics not claimed.  
**Portfolio:** [GitHub URL after publish] · LinkedIn: https://www.linkedin.com/in/leroy-garvin-49443b423/

---

## E. Sign-off

| Gate | Ready? |
|------|--------|
| Security (Public) | Yes — pending re-scan after screenshots |
| Evidence (Public screenshots) | **No** |
| GitHub publish | **No — blocked on Evidence** |
| LinkedIn portfolio link | **No — blocked on GitHub** |

**Nothing in this checklist authorizes publishing.** Complete B3, then publish intentionally.
