from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from app.config import ROOT

LOG_PATH = ROOT / "data" / "agent_actions.log"
LOCK_PATH = ROOT / "data" / "agent_run.lock"


def log_action(event: str, **details: Any) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    line = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "event": event,
        **details,
    }
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(line, ensure_ascii=False) + "\n")


def acquire_run_lock(*, force: bool = False, max_age_seconds: int = 1800) -> bool:
    """Prevent duplicate concurrent agent searches. force=True for RUN NOW override of stale locks."""
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    if LOCK_PATH.exists() and not force:
        try:
            data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
            started = datetime.fromisoformat(str(data.get("started_at", "")).replace("Z", ""))
            age = (datetime.utcnow() - started).total_seconds()
            if age < max_age_seconds and data.get("status") == "running":
                return False
        except Exception:  # noqa: BLE001
            pass
    LOCK_PATH.write_text(
        json.dumps(
            {
                "status": "running",
                "started_at": datetime.utcnow().isoformat() + "Z",
                "force": force,
            }
        ),
        encoding="utf-8",
    )
    log_action("run_lock_acquired", force=force)
    return True


def release_run_lock(**extra: Any) -> None:
    payload = {
        "status": "idle",
        "finished_at": datetime.utcnow().isoformat() + "Z",
        **extra,
    }
    LOCK_PATH.write_text(json.dumps(payload), encoding="utf-8")
    log_action("run_lock_released", **extra)
