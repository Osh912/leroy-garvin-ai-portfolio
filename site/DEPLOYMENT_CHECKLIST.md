# Deployment Checklist — Web Portfolio (`site/`)

**Updated:** 2026-08-01

## ✅ Completed
- [x] Static recruiter site (Home, Projects ×5, Resume, About, Contact, Legal, 404)
- [x] Working navigation + mobile menu
- [x] Resume PDF download (`assets/resume/Leroy_Garvin_Jr_AI_Operations_Resume.pdf`)
- [x] GH-X product sample images
- [x] Architecture SVG diagrams (GH-X, Voice, n8n, Airtable)
- [x] Voice documentation evidence screenshots (sanitized)
- [x] Honest Functional Build labeling (no invented metrics)
- [x] `vercel.json` (root + site)
- [x] `.nojekyll` for GitHub Pages
- [x] Responsive CSS (desktop + mobile)

## 🟡 Still Needs Work (optional strength, not blockers for soft launch)
- [ ] Capture sanitized **live n8n canvas** screenshots (N8-01–N8-04)
- [ ] Capture sanitized **Airtable UI** screenshots (AT-01–AT-02)
- [ ] Exact employment start date when verified
- [ ] Initialize git remote / push when you choose to publish
- [ ] LinkedIn Featured link after GitHub/Vercel URL is live

## 🚀 Ready to Deploy
| Target | How |
|--------|-----|
| **Vercel** | Import repo → Root Directory `site` (or use root `vercel.json` with `outputDirectory: site`) → Deploy |
| **GitHub Pages** | Settings → Pages → Deploy from `/site` folder (or `gh-pages` branch containing site contents). Ensure `.nojekyll` is present. |

**Pre-flight:** Confirm no `.env`, workflow JSON, or Private Master content is in `site/`.
