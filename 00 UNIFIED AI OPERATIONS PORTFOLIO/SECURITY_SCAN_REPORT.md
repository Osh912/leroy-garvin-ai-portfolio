# SECURITY_SCAN_REPORT.md

**Date:** 2026-07-20

## Policy
- Raw n8n JSON: Private only (23 canonical copies)
- Public JSON count: **0** (must remain 0)
- Downloads duplicates: excluded from portfolio copies
- ServiceFlowAI `.env*`: not copied into portfolio

## Public portfolio scan
| File | Line | Pattern | Assessment | Public-safe |
|------|-----:|---------|------------|-------------|
| `00 PUBLIC RECRUITER PORTFOLIO/README.md` | 5 | phone | Approved public contact | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/README.md` | 6 | email | Approved public contact | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/10 Legal and Usage Notice/COPYRIGHT_AND_USAGE_NOTICE.md` | 12 | email | Approved public contact | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/01 Resume/FINAL_MASTER_RESUME.md` | 10 | phone | Approved public contact | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/01 Resume/FINAL_MASTER_RESUME.md` | 10 | email | Approved public contact | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/02 About and Contact/README.md` | 5 | phone | Approved public contact | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/02 About and Contact/README.md` | 6 | email | Approved public contact | Yes |
| `00 PUBLIC RECRUITER PORTFOLIO/02 About and Contact/RECRUITER_REVIEW_NOTICE.md` | 10 | email | Approved public contact | Yes |

## Verdict
- No raw secrets detected in public markdown beyond **approved contact** phone/email.
- Private ID appendix remains under Private Master only.
- Before GitHub: re-scan after adding any screenshots.

## Redaction / containment actions
- No new secret values published.
- Unified docs reference Airtable/n8n without embedding base/table IDs in public unified files.
- **2026-07-20 final audit:** Moved stray `00 UNIFIED AI OPERATIONS PORTFOLIO/_meta.json` → `00 PRIVATE MASTER PORTFOLIO/11 Audit Reports/_unified_workflow_meta.json`. JSON outside Private after move: **0**.

## Final recruiter audit
See `FINAL_RECRUITER_AUDIT.md` and `FINAL_PUBLICATION_CHECKLIST.md` in this Unified folder (copies also under Private `11 Audit Reports/`).
