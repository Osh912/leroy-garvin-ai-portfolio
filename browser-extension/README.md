# Job Machine Safe Autofill (Chrome MV3)

Local browser companion for Leroy Garvin Jr’s Job Machine.  
**Never auto-submits. Never bypasses CAPTCHA/login/security. Never invents answers.**

Communicates only with `http://127.0.0.1:8787` by default.

## A. Browser extension folder

```
browser-extension/
```

## B. Installation steps

1. Start Job Machine:
   ```bash
   cd job-machine
   source .venv/bin/activate
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8787
   ```
2. Chrome → `chrome://extensions` → enable **Developer mode**
3. **Load unpacked** → select this `browser-extension/` folder
4. In Job Machine: **Prepare Application** → **Open Application**
5. On the application page, review the Safe Autofill preview → **Confirm Autofill**
6. Complete sensitive/custom questions yourself → submit yourself
7. Click **Mark as Submitted** (extension panel or Job Machine)

Fixture pages for local adapter checks:  
`http://127.0.0.1:8787/fixtures/greenhouse.html` (and lever, ashby, smartrecruiters, workday, indeed, linkedin, generic)

## C. Platforms supported

| Platform | Adapter |
|----------|---------|
| Greenhouse | `adapters/greenhouse.js` |
| Lever | `adapters/lever.js` |
| Ashby | `adapters/ashby.js` |
| SmartRecruiters | `adapters/smartrecruiters.js` |
| Workday | `adapters/workday.js` |
| Indeed company pages | `adapters/indeed.js` |
| LinkedIn external/apply forms | `adapters/linkedin.js` |
| Generic career forms | `adapters/generic.js` |

## D. Permissions requested

- `storage` — local field-map corrections only
- `activeTab` / `scripting` — run companion UI on the open application tab
- Host access to Job Machine localhost + common ATS hosts listed in `manifest.json`
- **No** remote telemetry, **no** credential storage, **no** history collection

## E. Fields autofilled (after Confirm Autofill)

Only when present in verified Job Machine profile:

- First name, Last name, Email, Phone  
- Country, City, State  
- ZIP code **only if verified in profile** (currently unset — never invented)  
- LinkedIn URL, Portfolio URL, GitHub URL (profile-verified)  
- Current job title  

Resume/cover are prepared as **job-specific files** for manual upload (company+role verified in filename).

## F. Fields requiring manual review

- File uploads (resume / cover / work samples)  
- Why this role / company drafts (Suggested Answer → edit → paste yourself)  
- Work authorization / sponsorship  
- Salary / compensation  
- Disability / veteran / demographic / EEO  
- Criminal / background disclosures  
- Education / certifications when not in verified profile  
- Start date (never invented)  
- Any unmatched custom screening question  
- **Final Submit Application button** (never clicked by the extension)

## G. Safety controls

- Explicit **Confirm Autofill** required before any fill  
- `neverClickSubmit` hard rule in `lib/safety.js`  
- Sensitive-question classifier blocks auto answers  
- Wrong-company packet files refused by API (`verify_file_belongs_to_application`)  
- Safety checklist before submit (company, title, resume/cover versions, portfolio, LinkedIn, contact, claims scan)  
- Activity log written locally under `job-machine/data/autofill_activity.log`  
- No public deployment of this extension

## H. Test results

Run from `job-machine/`:

```bash
pytest -q tests/test_safe_autofill.py
```

Covers platform detection, fixture field mapping, sensitive/manual classification, wrong-file rejection, confirm/session contract, suggested-answer policy, mark-submitted tracking, and submit-guard presence in extension source.

## I. Known limitations

- ATS DOM structures change often — use Options → manual field-map corrections  
- LinkedIn Easy Apply / logged-in walls are not automated; external forms only  
- CAPTCHA, SSO, MFA, and identity checks always remain human  
- PDF generation depends on local `reportlab`; `.txt`/`.md` always available  
- File inputs cannot be set by extensions for security — download then attach manually  
- ZIP code not autofilled until you add a verified value to `profile.json`  
- Extension is **local unpacked** only — do not publish to Chrome Web Store
