from __future__ import annotations

import asyncio
import logging
from datetime import datetime, time
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import SessionLocal, init_db
from app.routers.api import router as api_router

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "static"
EXTENSION_FIXTURES = ROOT.parent / "browser-extension" / "fixtures"
logger = logging.getLogger("job_machine")

app = FastAPI(
    title="Interview Pipeline — Leroy Garvin Jr",
    description="AI Interview Pipeline: verified remote jobs → packets → prep → tracker. Never auto-applies.",
    version="2.0.0",
)

# Local Safe Autofill companion (Chrome MV3) — localhost + extension origins only.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8787",
        "http://localhost:8787",
    ],
    allow_origin_regex=r"^chrome-extension://[a-z]+$",
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

_refresh_task: asyncio.Task | None = None


async def _morning_loop() -> None:
    """Every morning (~8:00 local) refresh remote jobs and prepare Top 10 packets."""
    from app.services.interview_pipeline import morning_refresh

    last_run_date = None
    while True:
        try:
            now = datetime.now()
            target = time(8, 0)
            if now.time() >= target and last_run_date != now.date():
                db = SessionLocal()
                try:
                    log = await morning_refresh(db, prepare_packets=True)
                    logger.info(
                        "Morning refresh complete: fetched=%s matched=%s packets=%s",
                        log.get("fetched"),
                        log.get("matched"),
                        log.get("packets_prepared"),
                    )
                    last_run_date = now.date()
                finally:
                    db.close()
        except Exception:  # noqa: BLE001
            logger.exception("Morning refresh failed")
        await asyncio.sleep(60 * 15)  # check every 15 minutes


@app.on_event("startup")
async def on_startup() -> None:
    global _refresh_task
    (ROOT / "data").mkdir(parents=True, exist_ok=True)
    (ROOT / "data" / "interview_packets").mkdir(parents=True, exist_ok=True)
    init_db()
    _refresh_task = asyncio.create_task(_morning_loop())


@app.on_event("shutdown")
async def on_shutdown() -> None:
    global _refresh_task
    if _refresh_task:
        _refresh_task.cancel()
        try:
            await _refresh_task
        except asyncio.CancelledError:
            pass


app.include_router(api_router)
app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")
if EXTENSION_FIXTURES.exists():
    app.mount("/fixtures", StaticFiles(directory=str(EXTENSION_FIXTURES)), name="fixtures")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "interview", "auto_apply": "false"}
