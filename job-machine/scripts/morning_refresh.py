#!/usr/bin/env python3
"""Morning Interview Pipeline refresh — cron-friendly. Never auto-applies."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.database import SessionLocal, init_db
from app.services.interview_pipeline import morning_refresh


async def main() -> None:
    init_db()
    db = SessionLocal()
    try:
        result = await morning_refresh(db, prepare_packets=True)
        print(json.dumps({
            "ok": True,
            "fetched": result["fetched"],
            "matched": result["matched"],
            "packets": result["packets_prepared"],
            "auto_apply": False,
            "log": str(ROOT / "data" / "morning_refresh_last.json"),
        }, indent=2))
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
