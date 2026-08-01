# GITHUB_PUBLICATION_SAFETY_CHECKLIST.md

**Date:** 2026-07-20  
**GitHub initialized/published by this process:** **No** (forbidden until manual approval)

## Required before any public GitHub publish
- [ ] Public repository contains no raw n8n JSON exports
- [ ] Public repository contains no .env files
- [ ] Public repository contains no secrets
- [ ] Public repository contains no customer information
- [ ] Public repository contains no complete proprietary prompts
- [ ] Public repository contains no internal databases
- [ ] Public repository contains no private source files
- [ ] Public repository uses sanitized screenshots only
- [ ] Public repository contains copyright and usage notice
- [ ] Public repository contains a clear README
- [ ] Private master portfolio is **not** inside the public Git repository
- [ ] Git history scanned before publication
- [ ] `.gitignore` present (see public portfolio `.gitignore`)
- [ ] ServiceFlowAI still excluded from public repo

## Recommended publish unit
Publish **only** `00 PUBLIC RECRUITER PORTFOLIO/` as the git root (or copy it to a clean folder), never the full workspace containing private JSON.
