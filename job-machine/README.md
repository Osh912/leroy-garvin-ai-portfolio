# Job Machine — Leroy Garvin Jr (Production)

AI Interview Pipeline for verified **remote US** roles in AI Operations, Workflow Automation, Technical Support, Solutions Engineering, Customer Success, Prompt Engineering, and related SaaS roles.

## Production rules

- No placeholder / demo employers (Acme, Example Corp, etc.)
- **Free sources only** — Greenhouse, Lever, Ashby, Workable + free aggregators (RemoteOK, Remotive, Jobicy)
- Free discovery/manual: LinkedIn Easy Apply, Indeed, ZipRecruiter, Google Jobs, Built In, Wellfound, Otta
- **Permanently excluded:** We Work Remotely, FlexJobs, Remote Rocketship, and any pay-to-apply / premium board
- 100% remote · United States only · no staffing agencies without a named employer
- Active posting URL check before display
- Transparent **Match Score** — never invents interview probabilities
- Auto-apply is always OFF — applications require explicit approval

## Run locally

```bash
cd job-machine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8787
```

Open http://127.0.0.1:8787

Morning refresh (cron):

```bash
PYTHONPATH=. python scripts/morning_refresh.py
```
