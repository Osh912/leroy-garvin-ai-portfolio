# Job Machine — Leroy Garvin Jr (Production)

AI Interview Pipeline for verified **remote** roles in AI Operations, Workflow Automation, Technical Support, Solutions Engineering, Customer Success, and AI Implementation.

## Production rules

- No placeholder / demo employers (Acme, Example Corp, etc.)
- Only live sources (RemoteOK, We Work Remotely, Greenhouse, Lever, Ashby, Remotive, Jobicy)
- Active posting URL check before display
- Transparent **Match Score** (skill · resume · portfolio · experience · remote · salary) — never invents interview probabilities
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
