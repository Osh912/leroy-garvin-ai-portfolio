from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from app.config import ROOT
from app.services.filters import normalize

CACHE_PATH = ROOT / "data" / "company_cache.json"
TTL_SECONDS = 60 * 60 * 12  # 12 hours


def _load() -> dict[str, Any]:
    if not CACHE_PATH.exists():
        return {}
    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _save(data: dict[str, Any]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def get_cached_company(company: str) -> dict[str, Any] | None:
    key = normalize(company)
    data = _load()
    row = data.get(key)
    if not row:
        return None
    if time.time() - float(row.get("cached_at", 0)) > TTL_SECONDS:
        return None
    return row.get("payload")


def set_cached_company(company: str, payload: dict[str, Any]) -> None:
    key = normalize(company)
    data = _load()
    data[key] = {"cached_at": time.time(), "payload": payload}
    _save(data)
