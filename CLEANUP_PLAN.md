# CLEANUP_PLAN.md — Safe Portfolio Cleanup Plan

**Based on:** `DUPLICATE_REPORT.md`  
**Status:** PLAN ONLY — do not delete, rename, move, or merge until explicitly approved  
**Preferred numbered folders (keep):**  
`01 Resume` · `02 LinkedIn` · `03 AI Voice Assistant` · `04 GH-X` · `05 Red Flag Diaries` · `06 n8n Workflow` · `07 Airtable` · `08 Screenshots` · `09 Certificates` · `10 References`

**Target root folder (only these files):**
- `README.md`
- `Career_Profile.md`
- `Career_Strategy.md`
- `Interview_Stories.md`
- `Cover_Letter_Template.md`
- `Recruiter_FAQ.md`
- `DUPLICATE_REPORT.md`

Also retain at root after cleanup (planning docs):
- `CLEANUP_PLAN.md` (this file)

---

## Safety Rules for Future Execution

1. Never delete a file until unique content is confirmed preserved in the primary file.
2. Archive first; permanent delete only after a review pass.
3. Update all internal links after moves.
4. One duplicate group at a time.
5. Do not invent content while merging—preserve truthful wording only.

**Proposed archive location (create only when cleanup is approved):**  
`_Archive/YYYY-MM-DD_cleanup/`

---

## Target End-State Map

### Root
| File | Action |
|------|--------|
| `README.md` | Primary portfolio entry (absorbs PORTFOLIO_README + Portfolio_Index navigation) |
| `Career_Profile.md` | Keep as-is location |
| `Career_Strategy.md` | Keep as-is location |
| `Interview_Stories.md` | Primary interview deep-prep (absorbs unique cheatsheet items if needed) |
| `Cover_Letter_Template.md` | Keep as-is location |
| `Recruiter_FAQ.md` | Primary recruiter screening doc (absorbs unique Recruiter Guide items) |
| `DUPLICATE_REPORT.md` | Keep |
| `CLEANUP_PLAN.md` | Keep |

### Folders
| Folder | Final name | Notes |
|--------|------------|-------|
| `01 Resume` | `01 Resume` | Holds all resumes + ATS keywords |
| `02 Linkin` | `02 LinkedIn` | Rename only when cleanup approved |
| `03 AI Voice Assistant` | `03 AI Voice Assistant` | Keep |
| `04 GH-X` | `04 GH-X` | Keep |
| `05 Red Flag Diaries` | `05 Red Flag Diaries` | Keep excluded status; optional later archive |
| `06 n8n Workflow` | `06 n8n Workflow` | Keep preferred name |
| `07 Airtable` | `07 Airtable` | Keep |
| `08 Screenshots` | `08 Screenshots` | Rename evidence files for consistency |
| `09 Certificates` | `09 Certificates` | Keep |
| `10 References` | `10 References` | Keep both active + template |

---

## Duplicate Group Plans

---

### Group 1 — Master Resume

| Field | Decision |
|-------|----------|
| **1. Primary file** | `FINAL_MASTER_RESUME.md` |
| **2. Merge into primary** | `01 Resume/Master_AI_Resume.md` |
| **3. Unique content to preserve** | From folder master: any bullets/sections not already in FINAL (especially project block formatting, tools line, additional information). From FINAL: employer-ready formatting, role targeting list including AI Support Engineer, qualitative “reduced common failure patterns” wording. |
| **4. Exact final file name** | `Master_AI_Resume.md` |
| **5. Exact final folder location** | `01 Resume/Master_AI_Resume.md` |
| **6. Archive duplicate after merging?** | **Yes.** Archive root `FINAL_MASTER_RESUME.md` after content is merged into `01 Resume/Master_AI_Resume.md` and links updated. |

**Notes:** Role-specific resumes stay in `01 Resume/` and are not duplicates of the master.

---

### Group 2 — LinkedIn Profile Pack

| Field | Decision |
|-------|----------|
| **1. Primary file** | `FINAL_LINKEDIN_PROFILE.md` (publish pack) **plus** keep modular drafts as editable source |
| **2. Merge into primary** | Sync unique content **both ways once**, then designate: publish pack = `Final_LinkedIn_Profile.md`; working modules remain `Headline.md`, `About.md`, `Experience.md`, `Skills.md` |
| **3. Unique content to preserve** | From FINAL: consolidated About, Experience bullets, Open to Work titles, Featured recommendations, truthfulness notes. From folder: ranked headlines (20 options), alternate About versions A/B, skills endorsement strategy, “skills not to list,” keyword coverage checklist. |
| **4. Exact final file name** | `Final_LinkedIn_Profile.md` |
| **5. Exact final folder location** | `02 LinkedIn/Final_LinkedIn_Profile.md` |
| **6. Archive duplicate after merging?** | **Yes for root copy only.** Archive root `FINAL_LINKEDIN_PROFILE.md`. **Do not archive** `Headline.md`, `About.md`, `Experience.md`, `Skills.md`—they remain active working files in `02 LinkedIn/`. |

**Also:** Rename folder `02 Linkin` → `02 LinkedIn` during this group’s execution.

---

### Group 3 — ATS Keywords

| Field | Decision |
|-------|----------|
| **1. Primary file** | `ATS_KEYWORDS_MASTER.md` |
| **2. Merge into primary** | `ATS_Keywords.md` **and** overlapping keyword lists from `01 Resume/Resume_Keyword_Bank.md` |
| **3. Unique content to preserve** | From `ATS_Keywords.md`: any placement rules or tool notes not in MASTER. From Keyword Bank: role-specific packs and “keywords to avoid.” From MASTER: power phrases, forbidden keywords, resume-variant mapping table, AI Support Engineer keywords. |
| **4. Exact final file name** | `ATS_Keywords_Master.md` |
| **5. Exact final folder location** | `01 Resume/ATS_Keywords_Master.md` |
| **6. Archive duplicate after merging?** | **Yes.** Archive root `ATS_KEYWORDS_MASTER.md` and root `ATS_Keywords.md`. |

**After merge — Keyword Bank fate:**

| Field | Decision |
|-------|----------|
| **1. Primary file** | Slim role-mapping file retained |
| **2. Merge into primary** | N/A (content already absorbed into ATS master) |
| **3. Unique content to preserve** | Keep only role→keyword mapping table if still useful; otherwise archive entire bank |
| **4. Exact final file name** | `Resume_Keyword_Bank.md` (thin mapping only) **or** archive if fully redundant |
| **5. Exact final folder location** | `01 Resume/Resume_Keyword_Bank.md` |
| **6. Archive duplicate after merging?** | **Maybe.** Archive only if every unique mapping exists in `ATS_Keywords_Master.md`. Prefer keep thin mapping file. |

---

### Group 4 — Portfolio Entry / Navigation

| Field | Decision |
|-------|----------|
| **1. Primary file** | `README.md` |
| **2. Merge into primary** | `PORTFOLIO_README.md` + navigation/status tables from `Portfolio_Index.md` |
| **3. Unique content to preserve** | From PORTFOLIO_README: recruiter start path, folder status table, truthfulness standard, candidate summary, next steps. From Portfolio_Index: complete link inventory and completion status grid. From current README: short recruiter/candidate quick links. |
| **4. Exact final file name** | `README.md` |
| **5. Exact final folder location** | Root: `README.md` |
| **6. Archive duplicate after merging?** | **Yes.** Archive `PORTFOLIO_README.md` and `Portfolio_Index.md` after README absorbs unique navigation content. |

---

### Group 5 — Recruiter Materials

| Field | Decision |
|-------|----------|
| **1. Primary file** | `Recruiter_FAQ.md` |
| **2. Merge into primary** | Unique evaluation content from `RECRUITER_GUIDE.md` |
| **3. Unique content to preserve** | From FAQ: screening Q&A, 30-second pitch, salary framing, “what not to claim.” From Guide: best-fit role ranking, what to review first, verified skills table, hiring recommendation framework, suggested interview questions, work-sample ideas, “red flags to avoid misreading.” |
| **4. Exact final file name** | `Recruiter_FAQ.md` |
| **5. Exact final folder location** | Root: `Recruiter_FAQ.md` |
| **6. Archive duplicate after merging?** | **Yes.** Archive `RECRUITER_GUIDE.md` after unique sections are merged into FAQ. |

**Rationale:** Root may contain only `Recruiter_FAQ.md` among recruiter docs; Guide content must live inside FAQ or be lost.

---

### Group 6 — Interview Prep

| Field | Decision |
|-------|----------|
| **1. Primary file** | `Interview_Stories.md` |
| **2. Merge into primary** | Unique quick-reference items from `INTERVIEW_CHEATSHEET.md` that are not already in Stories |
| **3. Unique content to preserve** | From Stories: full STAR stories, follow-ups, tips. From Cheatsheet: 30-second pitch, booking stages cold list, 9-step QA method, root-cause buckets, role-specific angles, questions to ask them, red lines, “no tech company experience” response, closing line. |
| **4. Exact final file name** | `Interview_Stories.md` |
| **5. Exact final folder location** | Root: `Interview_Stories.md` |
| **6. Archive duplicate after merging?** | **Yes.** Archive `INTERVIEW_CHEATSHEET.md` after unique cheatsheet sections are added as a “Quick Reference” section at the top of `Interview_Stories.md`. |

**Alternative (if you prefer two files later):** Keep a non-root cheatsheet under a new interview subfolder—but preferred root list does not include it, so plan defaults to merge + archive.

---

### Group 7 — Career Positioning vs Resume (NOT a merge of whole files)

| Field | Decision |
|-------|----------|
| **1. Primary file** | `Career_Profile.md` (positioning) and `01 Resume/Master_AI_Resume.md` (application) |
| **2. Merge into primary** | Do **not** merge files whole. Optionally sync summary wording so they stay consistent. |
| **3. Unique content to preserve** | Profile: target roles, strengths, project highlights, tailoring notes. Resume: ATS bullets, project blocks, tools line. |
| **4. Exact final file name** | `Career_Profile.md` and `Master_AI_Resume.md` |
| **5. Exact final folder location** | Root `Career_Profile.md`; `01 Resume/Master_AI_Resume.md` |
| **6. Archive duplicate after merging?** | **No.** Both remain active. |

---

### Group 8 — Career Strategy vs Recruiter FAQ (NOT a full merge)

| Field | Decision |
|-------|----------|
| **1. Primary file** | `Career_Strategy.md` |
| **2. Merge into primary** | Do **not** merge with Recruiter FAQ. Optionally copy only recruiter-facing score/verdict snippets into FAQ if missing. |
| **3. Unique content to preserve** | Strategy: 90-day plan, salary bands, company tiers, weekly application plan, roadmap, portfolio score, top 20 improvements. FAQ: screening answers. |
| **4. Exact final file name** | `Career_Strategy.md` |
| **5. Exact final folder location** | Root: `Career_Strategy.md` |
| **6. Archive duplicate after merging?** | **No.** |

---

### Group 9 — References Template vs Active References

| Field | Decision |
|-------|----------|
| **1. Primary file** | Keep **both** (not true content duplicates) |
| **2. Merge into primary** | No content merge required |
| **3. Unique content to preserve** | `References.md` = policy + active status. `Professional_References_Template.md` = fillable form + notification message. |
| **4. Exact final file names** | `References.md` and `References_Template.md` |
| **5. Exact final folder location** | `10 References/References.md` and `10 References/References_Template.md` |
| **6. Archive duplicate after merging?** | **No.** Rename template only (when approved): `Professional_References_Template.md` → `References_Template.md`. |

---

### Group 10 — Same Basename Across Projects (NOT duplicates)

| Field | Decision |
|-------|----------|
| **1. Primary file** | Each project’s own `Project_Overview.md`, `Business_Problem.md`, etc. |
| **2. Merge into primary** | Do not merge across `03` / `04` / `05` |
| **3. Unique content to preserve** | All project-specific content |
| **4. Exact final file name** | Keep current basenames |
| **5. Exact final folder location** | Stay inside `03 AI Voice Assistant`, `04 GH-X`, `05 Red Flag Diaries` |
| **6. Archive duplicate after merging?** | **No.** |

---

### Group 11 — Screenshot Evidence Naming (rename only; no merge)

| Current file | Primary? | Merge? | Unique content | Exact final name | Exact final location | Archive? |
|--------------|----------|--------|----------------|------------------|----------------------|----------|
| `08 Screenshots/Screenshot_Index.md` | Yes | No | Index + privacy checklist | `Screenshot_Index.md` | `08 Screenshots/` | No |
| `08 Screenshots/AI_Voice_Assistant.md` | Yes | No | Voice evidence checklist | `AI_Voice_Assistant_Evidence.md` | `08 Screenshots/` | No (rename only) |
| `08 Screenshots/GHX_Workflow.md` | Yes | No | GH-X evidence checklist | `GH-X_Workflow_Evidence.md` | `08 Screenshots/` | No (rename only) |
| `08 Screenshots/n8n_Workflow.md` | Yes | No | n8n evidence checklist | `n8n_Workflow_Evidence.md` | `08 Screenshots/` | No (rename only) |
| `08 Screenshots/Airtable_System.md` | Yes | No | Airtable evidence checklist | `Airtable_System_Evidence.md` | `08 Screenshots/` | No (rename only) |
| `08 Screenshots/Cursor_Development.md` | Yes | No | Cursor evidence checklist | `Cursor_Development_Evidence.md` | `08 Screenshots/` | No (rename only) |

---

### Group 12 — Red Flag Diaries (excluded project)

| Field | Decision |
|-------|----------|
| **1. Primary file** | `05 Red Flag Diaries/Project_Overview.md` (exclusion notice) |
| **2. Merge into primary** | No merge with other projects |
| **3. Unique content to preserve** | Exclusion status language in all five files |
| **4. Exact final file name** | Keep current names while folder remains |
| **5. Exact final folder location** | `05 Red Flag Diaries/` (preferred structure keeps this folder) |
| **6. Archive duplicate after merging?** | **Optional later.** May move entire folder to `_Archive/Red_Flag_Diaries/` in a future pass; not required for root cleanup. |

---

## Root File Relocation Plan (Non-Duplicate Moves)

These root files are not always “duplicates,” but they must leave root to match the preferred root list.

| Current root file | Action | Final name | Final location | Archive original root path? |
|-------------------|--------|------------|----------------|-----------------------------|
| `FINAL_MASTER_RESUME.md` | Merge → then archive | `Master_AI_Resume.md` | `01 Resume/` | Yes |
| `FINAL_LINKEDIN_PROFILE.md` | Move/sync → then archive root | `Final_LinkedIn_Profile.md` | `02 LinkedIn/` | Yes |
| `ATS_KEYWORDS_MASTER.md` | Merge → move | `ATS_Keywords_Master.md` | `01 Resume/` | Yes (after merge) |
| `ATS_Keywords.md` | Merge → archive | — | — | Yes |
| `PORTFOLIO_README.md` | Merge into README → archive | — | — | Yes |
| `Portfolio_Index.md` | Merge into README → archive | — | — | Yes |
| `RECRUITER_GUIDE.md` | Merge into Recruiter_FAQ → archive | — | — | Yes |
| `INTERVIEW_CHEATSHEET.md` | Merge into Interview_Stories → archive | — | — | Yes |
| `Cover_Letter_Template.md` | Keep | `Cover_Letter_Template.md` | Root | No |
| `Career_Profile.md` | Keep | `Career_Profile.md` | Root | No |
| `Career_Strategy.md` | Keep | `Career_Strategy.md` | Root | No |
| `Interview_Stories.md` | Keep (absorbs cheatsheet) | `Interview_Stories.md` | Root | No |
| `Recruiter_FAQ.md` | Keep (absorbs guide) | `Recruiter_FAQ.md` | Root | No |
| `README.md` | Keep (absorbs nav guides) | `README.md` | Root | No |
| `DUPLICATE_REPORT.md` | Keep | `DUPLICATE_REPORT.md` | Root | No |
| `CLEANUP_PLAN.md` | Keep | `CLEANUP_PLAN.md` | Root | No |

**Note:** `Cover_Letter_Template.md` already matches preferred root list. If a copy later exists under `01 Resume/`, keep only the root copy unless you prefer resume-folder placement—current plan keeps it at root.

---

## Folder Rename Plan (No Content Change)

| Current | Final | When |
|---------|-------|------|
| `02 Linkin` | `02 LinkedIn` | With Group 2 execution |

No other folder renames in this plan (per preferred structure).

---

## Safe Execution Order (For Future Approval)

Execute only after you say to proceed.

1. **Create** `_Archive/YYYY-MM-DD_cleanup/`
2. **Group 3** — ATS keywords merge → move master to `01 Resume/` → archive root keyword duplicates
3. **Group 1** — Master resume merge → ensure canonical at `01 Resume/Master_AI_Resume.md` → archive root FINAL resume
4. **Group 2** — Rename `02 Linkin` → `02 LinkedIn`; sync LinkedIn pack; place `Final_LinkedIn_Profile.md` in folder; archive root FINAL LinkedIn
5. **Group 4** — Merge navigation into `README.md`; archive PORTFOLIO_README + Portfolio_Index
6. **Group 5** — Merge Recruiter Guide into `Recruiter_FAQ.md`; archive RECRUITER_GUIDE
7. **Group 6** — Merge cheatsheet unique sections into `Interview_Stories.md`; archive INTERVIEW_CHEATSHEET
8. **Group 9** — Rename references template only
9. **Group 11** — Rename screenshot evidence files
10. **Link sweep** — Update links in README, resumes, project docs, Career_Strategy
11. **Verify** root contains only the preferred files (+ CLEANUP_PLAN / DUPLICATE_REPORT)
12. **Stop** — Do not permanently delete archives in this pass

---

## Post-Cleanup Root Checklist

After future execution, root should contain only:

- [ ] `README.md`
- [ ] `Career_Profile.md`
- [ ] `Career_Strategy.md`
- [ ] `Interview_Stories.md`
- [ ] `Cover_Letter_Template.md`
- [ ] `Recruiter_FAQ.md`
- [ ] `DUPLICATE_REPORT.md`
- [ ] `CLEANUP_PLAN.md` (recommended keep)

And folders:

- [ ] `01 Resume`
- [ ] `02 LinkedIn` (renamed from Linkin)
- [ ] `03 AI Voice Assistant`
- [ ] `04 GH-X`
- [ ] `05 Red Flag Diaries`
- [ ] `06 n8n Workflow`
- [ ] `07 Airtable`
- [ ] `08 Screenshots`
- [ ] `09 Certificates`
- [ ] `10 References`
- [ ] `_Archive/` (created during cleanup)

---

## Explicit Non-Actions in This Document

- No files deleted  
- No files renamed  
- No files moved  
- No files merged  
- No folders renamed  

**This file is a plan only.** Await explicit approval before executing any group.
