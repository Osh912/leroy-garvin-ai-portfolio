# Web portfolio (`site/`)

Static recruiter-facing site for **Leroy Garvin Jr — AI Career Portfolio**.  
This finishes the existing markdown vault for **GitHub Pages** and **Vercel**. It does not replace the vault.

## Local preview

```bash
cd site
python3 -m http.server 8080
# open http://localhost:8080
```

Or from the repo root:

```bash
npx serve site
```

## Deploy — Vercel

**Option A (recommended):** In the Vercel project settings, set **Root Directory** to `site`, then deploy. The included `site/vercel.json` configures static hosting.

**Option B:** Deploy from the repository root. The root `vercel.json` sets `"outputDirectory": "site"` so Vercel serves this folder as a static site.

Connect the GitHub repo → Import → Deploy. No build step required.

## Deploy — GitHub Pages

Publish the **`site`** folder as the Pages source (not the whole repo root).

1. Push this repository to GitHub.
2. **Settings → Pages → Build and deployment**
3. Source: **Deploy from a branch**
4. Branch: `main` (or your default), folder: **`/site`**  
   — or use a GitHub Action / `gh-pages` branch that contains only the contents of `site/`.
5. `.nojekyll` is included so GitHub Pages skips Jekyll processing.

After publish, the site URL will be like `https://<user>.github.io/<repo>/` when using a project site with `/site` as the published root (GitHub serves the folder contents at the site root).

## Resume PDF

The Resume page links to:

`assets/resume/Leroy_Garvin_Jr_AI_Operations_Resume.pdf`

If that file is missing, generate a PDF from  
`00 PUBLIC RECRUITER PORTFOLIO/01 Resume/FINAL_MASTER_RESUME.md`  
and place it at the path above. See `assets/resume/PDF_NOTE.txt`.

## Content honesty

- Status labels: **Functional Build** / **Evidence Pending** where true  
- No invented employers, metrics, revenue, certifications, or production claims  
- Red Flag Diaries and ServiceFlowAI are excluded from this public site  
- See `legal.html` for usage notice  

## Contact

- Leroy Garvin Jr — Savannah, Georgia, USA  
- (912) 901-6378 · AlignedVibesCo@gmail.com  
- [LinkedIn](https://www.linkedin.com/in/leroy-garvin-49443b423/)
