# Deployment Guide — Leroy Garvin Jr AI Career Portfolio

How to update and redeploy the **web portfolio** after launch.

**Live site source:** [`site/`](./site/)  
**Vercel config:** root [`vercel.json`](./vercel.json) → `outputDirectory: site`  
**GitHub Pages:** [`.github/workflows/pages.yml`](./.github/workflows/pages.yml)

---

## 1. What gets published

| Publish | Do not publish |
|---------|----------------|
| Everything under `site/` | `00 PRIVATE MASTER PORTFOLIO/` |
| Public markdown vault (`00 PUBLIC RECRUITER PORTFOLIO/`, resumes, guides) | `packages/`, `research/` |
| Architecture diagrams & placeholders | `.env`, JSON workflow exports, credentials |

Root `.gitignore` already blocks private/sensitive paths.

---

## 2. Edit content (typical updates)

1. Open the HTML page under `site/` (e.g. `site/projects/ghx.html`).
2. Keep claims honest: **Functional Build** / no invented metrics.
3. Replace placeholder images in `site/assets/images/placeholders/` with sanitized screenshots when ready.
4. Update resume PDF if experience changes:
   - Edit `FINAL_MASTER_RESUME.md`
   - Regenerate PDF into `site/assets/resume/Leroy_Garvin_Jr_AI_Operations_Resume.pdf`
5. Preview locally:

```bash
cd site
python3 -m http.server 8765
# open http://127.0.0.1:8765/
```

---

## 3. Commit and push to GitHub

```bash
cd "/Users/gh-x/Documents/Leroy Garvin Jr - AI Career Portfolio"
git status
git add -A
git commit -m "Update portfolio content."
git push origin main
```

GitHub Pages redeploys automatically via Actions when `site/**` changes (if the workflow is enabled).

---

## 4. Deploy / redeploy on Vercel

### First-time (CLI)

```bash
cd "/Users/gh-x/Documents/Leroy Garvin Jr - AI Career Portfolio"
npx vercel login
npx vercel --prod
```

Use root directory of the repo; `vercel.json` already points output to `site`.

### Dashboard

1. Import the GitHub repo in [vercel.com](https://vercel.com)
2. Framework Preset: **Other**
3. Root Directory: leave blank (repo root) — or set to `site` if you prefer
4. Build Command: empty  
5. Output Directory: `site` (if Root is repo root)
6. Deploy

Every push to `main` triggers a new production deployment when the project is linked.

---

## 5. Post-deploy checks (2 minutes)

- [ ] Home loads  
- [ ] Projects index + each project page  
- [ ] Resume page + **Download PDF**  
- [ ] About / Contact / Legal  
- [ ] Mobile nav menu  
- [ ] No 404s in browser Network tab  

---

## 6. Replace placeholders with real screenshots

1. Capture UI with secrets cropped (tokens, webhooks, customer PII, base IDs).
2. Export PNG/WebP ≤ ~1400px wide.
3. Overwrite the matching file in `site/assets/images/placeholders/` **or** add a new file and update the `<img src>` on the project page.
4. Update `00 PUBLIC RECRUITER PORTFOLIO/09 Sanitized Screenshots/SCREENSHOT_EVIDENCE_TRACKER.md`.
5. Commit + push (auto-redeploy).

---

## 7. Rollback

- **Vercel:** Deployments → select prior deployment → Promote to Production  
- **GitHub:** `git revert` the bad commit and push  

---

## 8. Contact block (keep in sync)

- Name: Leroy Garvin Jr  
- Email: AlignedVibesCo@gmail.com  
- Phone: (912) 901-6378  
- LinkedIn: https://www.linkedin.com/in/leroy-garvin-49443b423/  

Update these in `site/*.html` footers/headers and the PDF resume if they change.
