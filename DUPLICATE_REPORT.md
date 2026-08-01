# DUPLICATE_REPORT.md — AI Career Portfolio Audit

**Candidate:** Leroy Garvin Jr  
**Audit type:** Duplicate files, naming consistency, merge recommendations, folder structure  
**Rule applied:** No files deleted. No content modified. Report only.  
**Date:** July 16, 2026

---

## Executive Summary

The portfolio is content-rich but has **naming drift**, **overlapping root deliverables**, and **near-duplicate keyword/resume/LinkedIn sources**. Nothing needs emergency deletion. The cleanest fix is to designate one **canonical** file per purpose and mark older versions as draft/source—or merge them later.

| Issue type | Count (approx.) | Severity |
|------------|-----------------|----------|
| True content duplicates / near-duplicates | 8 pairs | High |
| Same filename in different folders (OK if intentional) | 5 basenames | Low |
| Naming inconsistencies | 12+ | Medium |
| Folder naming issues | 3 | Medium |
| Empty / excluded project clutter | 1 folder | Low–Medium |

---

## 1. Duplicate Files (Same Purpose / Near-Duplicate Content)

### A. High priority — root vs folder overlap

| File A | File B | Relationship | Recommendation |
|--------|--------|--------------|----------------|
| `FINAL_MASTER_RESUME.md` | `01 Resume/Master_AI_Resume.md` | Near-duplicate master resumes | **Merge into one canonical resume.** Keep `FINAL_MASTER_RESUME.md` as employer-facing; make `Master_AI_Resume.md` a pointer/alias OR deprecate after merge. |
| `FINAL_LINKEDIN_PROFILE.md` | `02 Linkin/About.md` + `Experience.md` + `Headline.md` + `Skills.md` | Consolidated LinkedIn vs split drafts | **Keep both temporarily:** `FINAL_LINKEDIN_PROFILE.md` = publish pack; folder files = working drafts. Later merge drafts into FINAL or generate FINAL from folder. |
| `ATS_KEYWORDS_MASTER.md` | `ATS_Keywords.md` | Same purpose, overlapping keyword banks | **Merge into `ATS_KEYWORDS_MASTER.md`.** Retire or convert `ATS_Keywords.md` to a short redirect note (later). |
| `ATS_KEYWORDS_MASTER.md` | `01 Resume/Resume_Keyword_Bank.md` | Overlapping ATS keywords | **Merge keyword lists into MASTER.** Keep Resume Keyword Bank only if it stays role-variant mapping (thinner file). |
| `PORTFOLIO_README.md` | `README.md` | Both act as entry docs | **Keep `README.md` as entry** (standard). Make `PORTFOLIO_README.md` the detailed guide OR merge into README. Avoid two “start here” docs. |
| `PORTFOLIO_README.md` | `Portfolio_Index.md` | Navigation / index overlap | **Merge index into PORTFOLIO_README or keep Portfolio_Index as TOC only.** One navigation source of truth. |
| `RECRUITER_GUIDE.md` | `Recruiter_FAQ.md` | Overlapping recruiter evaluation content | **Keep both if roles differ:** Guide = for recruiters; FAQ = screening answers. Clarify in titles. Do not merge blindly—complementary. |
| `INTERVIEW_CHEATSHEET.md` | `Interview_Stories.md` | Quick prep vs full STAR stories | **Keep both.** Cheatsheet = short; Stories = full. Cross-link only. |
| `Career_Profile.md` | `FINAL_MASTER_RESUME.md` (summary) | Profile summary overlaps resume summary | **Keep Career_Profile as internal positioning.** Resume remains application artifact. |
| `Career_Strategy.md` | `RECRUITER_GUIDE.md` / strategy sections | Strategy overlaps recruiter framing | **Keep Career_Strategy** as candidate planning doc; Recruiter Guide for external readers. |

### B. Medium priority — reference / template overlap

| File A | File B | Relationship | Recommendation |
|--------|--------|--------------|----------------|
| `10 References/References.md` | `10 References/Professional_References_Template.md` | Live refs vs template | **Keep both.** Rename for clarity: `References.md` = active list; `References_Template.md` = blank form. |

### C. Same basename across projects (NOT true duplicates)

These share names but live in different project folders. That is normal for case-study structure.

| Basename | Locations | Action |
|----------|-----------|--------|
| `Project_Overview.md` | `03`, `04`, `05` | Keep — standard case-study pattern |
| `Business_Problem.md` | `03`, `04`, `05` | Keep |
| `Workflow_Design.md` | `03`, `04` | Keep |
| `My_Role.md` | `03`, `04` | Keep |
| `Lessons_Learned.md` | `04`, `05` | Keep |

**Note:** Folder `05 Red Flag Diaries` is excluded from the active portfolio. Same filenames there are not harmful but add clutter until removed or archived.

### D. Screenshot naming vs project naming

| Screenshot file | Related project folder | Inconsistency |
|-----------------|------------------------|---------------|
| `08 Screenshots/AI_Voice_Assistant.md` | `03 AI Voice Assistant` | Underscores vs spaces; “AI Voice Assistant” vs “AI Voice Booking Assistant” in docs |
| `08 Screenshots/GHX_Workflow.md` | `04 GH-X` | `GHX` vs `GH-X` |
| `08 Screenshots/n8n_Workflow.md` | `06 n8n Workflow` | OK-ish; folder uses space + singular “Workflow” |

---

## 2. Files That Should Be Merged (Recommended Merge Plan)

Do **not** merge yet—this is the recommended plan for a later cleanup pass.

### Merge set 1 — Keywords
**Into:** `ATS_KEYWORDS_MASTER.md`  
**From:** `ATS_Keywords.md`, overlapping parts of `01 Resume/Resume_Keyword_Bank.md`  
**After merge:** Keep a thin `Resume_Keyword_Bank.md` with role→keyword mapping only, OR delete bank after confirming MASTER covers it.

### Merge set 2 — Master resume
**Into:** `FINAL_MASTER_RESUME.md` (canonical employer resume)  
**From:** `01 Resume/Master_AI_Resume.md`  
**After merge:** Role-specific resumes remain separate (`AI_Trainer_Resume.md`, etc.). Master folder file becomes symlink/redirect or is archived as `Master_AI_Resume_DRAFT.md`.

### Merge set 3 — Navigation
**Into:** One of:
- Option A: Expand `README.md` + keep `Portfolio_Index.md` as TOC  
- Option B: Keep `PORTFOLIO_README.md` as full guide + slim `README.md` pointing to it  

**Avoid:** Three overlapping entry docs (`README`, `PORTFOLIO_README`, `Portfolio_Index`) without clear hierarchy.

### Merge set 4 — LinkedIn (optional later)
**Into:** `FINAL_LINKEDIN_PROFILE.md` as publish source of truth  
**From:** `02 Linkin/*` drafts after one final sync  
**Or reverse:** Folder remains editable source; FINAL regenerated from folder.

### Do NOT merge
- `Interview_Stories.md` + `INTERVIEW_CHEATSHEET.md`
- `RECRUITER_GUIDE.md` + `Recruiter_FAQ.md` (different audiences)
- `Career_Strategy.md` + `Career_Profile.md`
- Project case-study files across `03` / `04` (intentionally parallel)

---

## 3. Better File Names

### Root files — naming consistency

| Current | Issue | Recommended name |
|---------|-------|------------------|
| `FINAL_MASTER_RESUME.md` | ALL CAPS style mixed with Title_Case | `00_Final_Master_Resume.md` or `Final_Master_Resume.md` |
| `FINAL_LINKEDIN_PROFILE.md` | Same | `Final_LinkedIn_Profile.md` |
| `PORTFOLIO_README.md` | Overlaps README | `Portfolio_Guide.md` (if README stays primary) |
| `Portfolio_Index.md` | OK | Keep, or `00_Portfolio_Index.md` |
| `ATS_KEYWORDS_MASTER.md` | ALL CAPS | `ATS_Keywords_Master.md` |
| `ATS_Keywords.md` | Duplicate purpose | Merge away; if kept: `ATS_Keywords_Legacy.md` |
| `INTERVIEW_CHEATSHEET.md` | ALL CAPS | `Interview_Cheatsheet.md` |
| `RECRUITER_GUIDE.md` | ALL CAPS | `Recruiter_Guide.md` |
| `Recruiter_FAQ.md` | Mixed casing vs GUIDE | `Recruiter_FAQ.md` (keep; align casing family) |
| `Interview_Stories.md` | OK | Keep |
| `Career_Profile.md` | OK | Keep |
| `Career_Strategy.md` | OK | Keep |
| `Cover_Letter_Template.md` | OK | Keep |
| `DUPLICATE_REPORT.md` | This report | Keep |

### Folder naming fixes

| Current | Issue | Recommended |
|---------|-------|-------------|
| `02 Linkin` | Typo / nonstandard | `02 LinkedIn` |
| `06 n8n Workflow` | Singular; inconsistent with “Workflows” | `06 n8n Workflows` |
| `03 AI Voice Assistant` | Docs often say “AI Voice Booking Assistant” | `03 AI_Voice_Booking_Assistant` or keep folder + standardize titles inside |
| `04 GH-X` | Screenshot uses `GHX` | Keep `04 GH-X`; rename screenshot to `GH-X_Workflow.md` |
| `05 Red Flag Diaries` | Excluded content still in active tree | Move to `_Archive/05_Red_Flag_Diaries` when ready |

### Resume file names

| Current | Recommended |
|---------|-------------|
| `Master_AI_Resume.md` | `Master_AI_Resume.md` (keep) OR archive as draft after FINAL merge |
| `AI_Data_Annotation_Resume.md` | Keep (matches target role) |
| `Remote_Operations_Resume.md` | Keep or rename `AI_Support_Remote_Operations_Resume.md` if targeting AI Support Engineer |

### Screenshot file names

| Current | Recommended |
|---------|-------------|
| `AI_Voice_Assistant.md` | `AI_Voice_Booking_Assistant_Evidence.md` |
| `GHX_Workflow.md` | `GH-X_Workflow_Evidence.md` |
| `n8n_Workflow.md` | `n8n_Workflow_Evidence.md` |
| `Airtable_System.md` | `Airtable_System_Evidence.md` |
| `Cursor_Development.md` | `Cursor_Development_Evidence.md` |
| `Screenshot_Index.md` | Keep |

### References

| Current | Recommended |
|---------|-------------|
| `Professional_References_Template.md` | `References_Template.md` |
| `References.md` | `References_Active.md` (optional clarity) |

---

## 4. Folder Organization Improvements

### Current structure (problems)
1. Too many “start here” files at root (README, PORTFOLIO_README, Portfolio_Index, RECRUITER_GUIDE).
2. Final deliverables mixed with working drafts at root.
3. `02 Linkin` spelling undermines professionalism.
4. Excluded Red Flag Diaries still sits in numbered active folders.
5. Screenshot evidence uses different naming than project folders.
6. Duplicate keyword systems at root and in Resume folder.

### Recommended clean structure for an AI Operations candidate

```text
AI_Operations_Portfolio_Leroy_Garvin_Jr/
│
├── README.md                          # Single entry point
├── 00_Recruiter/
│   ├── Recruiter_Guide.md
│   ├── Recruiter_FAQ.md
│   └── Portfolio_Index.md
│
├── 01_Resume/
│   ├── Final_Master_Resume.md         # Canonical
│   ├── AI_Operations_Resume.md
│   ├── AI_Trainer_Resume.md
│   ├── AI_Data_Annotation_Resume.md
│   ├── Prompt_Engineering_Resume.md
│   ├── Workflow_Automation_Resume.md  # optional rename from Remote_Ops
│   ├── Cover_Letter_Template.md
│   └── ATS_Keywords_Master.md
│
├── 02_LinkedIn/
│   ├── Final_LinkedIn_Profile.md      # Publish pack
│   ├── Headline.md
│   ├── About.md
│   ├── Experience.md
│   └── Skills.md
│
├── 03_Projects/
│   ├── AI_Voice_Booking_Assistant/
│   │   ├── 00_Project_Overview.md
│   │   ├── 01_Business_Problem.md
│   │   ├── 02_My_Role.md
│   │   ├── 03_Workflow_Design.md
│   │   ├── 04_Prompt_Engineering.md
│   │   ├── 05_Testing_and_QA.md
│   │   ├── 06_Challenges.md
│   │   ├── 07_Improvements.md
│   │   └── 08_Outcome.md
│   └── GH-X/
│       ├── 00_Project_Overview.md
│       ├── 01_Business_Problem.md
│       ├── 02_My_Role.md
│       ├── 03_Workflow_Design.md
│       ├── 04_AI_Automation.md
│       └── 05_Lessons_Learned.md
│
├── 04_Systems/
│   ├── n8n_Workflows/
│   │   ├── Workflow_Index.md
│   │   └── Workflow_Templates.md
│   └── Airtable/
│       ├── Airtable_Overview.md
│       └── Database_Structure.md
│
├── 05_Evidence/
│   ├── Screenshot_Index.md
│   ├── AI_Voice_Booking_Assistant_Evidence.md
│   ├── GH-X_Workflow_Evidence.md
│   ├── n8n_Workflow_Evidence.md
│   ├── Airtable_System_Evidence.md
│   ├── Cursor_Development_Evidence.md
│   └── /images/                       # actual PNGs later
│
├── 06_Interview/
│   ├── Interview_Stories.md
│   └── Interview_Cheatsheet.md
│
├── 07_Strategy/
│   ├── Career_Profile.md
│   ├── Career_Strategy.md
│   └── Duplicate_Report.md            # this file
│
├── 08_Credentials/
│   └── Certificate_Tracker.md
│
├── 09_References/
│   ├── References_Active.md
│   └── References_Template.md
│
└── _Archive/                          # not shared with recruiters
    └── Red_Flag_Diaries/              # excluded until documented
```

### Why this structure works for AI Operations candidates
- **Recruiter path is obvious:** README → Recruiter Guide → Final Resume → Projects → Evidence
- **One canonical resume** and **one keyword master**
- **Projects separated from systems** (n8n/Airtable are supporting systems, not always “projects”)
- **Evidence folder** makes proof easy to request in interviews
- **Archive** keeps incomplete work without polluting active portfolio
- **Consistent Title_Case / numbered folders** look intentional and ATS/recruiter friendly when shared as a zip or repo

---

## 5. Inconsistent Naming Patterns Found

| Pattern | Examples | Standardize to |
|---------|----------|----------------|
| ALL_CAPS finals | `FINAL_*`, `ATS_KEYWORDS_MASTER`, `PORTFOLIO_README` | `Title_Case.md` |
| Mixed LinkedIn spelling | `02 Linkin` vs “LinkedIn” in docs | `02 LinkedIn` |
| GH-X vs GHX | folder `GH-X`, screenshot `GHX_Workflow` | Always `GH-X` |
| Voice Assistant naming | folder “AI Voice Assistant” vs docs “AI Voice Booking Assistant” | Pick one product name |
| Spaces in folders | `03 AI Voice Assistant` | Prefer `03_AI_Voice_Booking_Assistant` for repos/zips |
| Underscores in files, spaces in folders | Mixed | Prefer underscores in both for portability |
| Singular vs plural | `06 n8n Workflow` | `06 n8n Workflows` |
| Evidence vs project filenames | `AI_Voice_Assistant.md` in Screenshots | Align to project product name |

---

## 6. Suggested Canonical “Source of Truth” Map

| Purpose | Canonical file (recommended) | Treat as draft / secondary |
|---------|------------------------------|----------------------------|
| Employer resume | `FINAL_MASTER_RESUME.md` | `01 Resume/Master_AI_Resume.md` |
| LinkedIn publish pack | `FINAL_LINKEDIN_PROFILE.md` | `02 Linkin/*` |
| ATS keywords | `ATS_KEYWORDS_MASTER.md` | `ATS_Keywords.md`, keyword bank overlap |
| Recruiter evaluation | `RECRUITER_GUIDE.md` | — |
| Screening answers | `Recruiter_FAQ.md` | — |
| Interview deep prep | `Interview_Stories.md` | — |
| Interview quick prep | `INTERVIEW_CHEATSHEET.md` | — |
| Portfolio entry | `README.md` | `PORTFOLIO_README.md` (or vice versa—pick one) |
| Navigation TOC | `Portfolio_Index.md` | — |
| Career positioning | `Career_Profile.md` | — |
| Job search plan | `Career_Strategy.md` | — |
| Primary project | `03 AI Voice Assistant/Project_Overview.md` | — |
| Secondary project | `04 GH-X/Project_Overview.md` | — |
| Excluded project | Archive later | `05 Red Flag Diaries/*` |

---

## 7. Priority Cleanup Order (When You Authorize Changes)

1. Rename `02 Linkin` → `02 LinkedIn`
2. Choose single entry doc hierarchy (README vs PORTFOLIO_README)
3. Merge keyword files into `ATS_KEYWORDS_Master`
4. Resolve master resume duplication (FINAL vs `Master_AI_Resume.md`)
5. Standardize GH-X / Voice Booking naming across screenshots and folders
6. Move Red Flag Diaries to `_Archive`
7. Optionally reorganize into the recommended AI Operations structure above

---

## 8. Cleanest Professional Structure Recommendation (Short Version)

For an **AI Operations candidate**, the cleanest portfolio is:

1. **One README** for humans  
2. **One Final Resume** + role variants  
3. **One LinkedIn publish pack**  
4. **Two proven projects** (Voice Booking + GH-X) with parallel case-study files  
5. **One systems section** (n8n + Airtable)  
6. **One evidence section** with screenshots  
7. **One interview section** (stories + cheatsheet)  
8. **One recruiter section** (guide + FAQ)  
9. **Archive** for incomplete work  

That structure signals process discipline—the same skill AI Operations hiring managers look for.

---

## 9. What Was Not Done (Per Instructions)

- No files deleted  
- No content rewritten  
- No renames executed  
- No folder moves executed  

**Next step when ready:** Approve a cleanup pass implementing Priority Cleanup Order items 1–6.
