from __future__ import annotations

from typing import Any

from app.services.filters import load_portfolio, normalize, text_blob


def match_portfolio(job: dict[str, Any], *, limit: int = 4) -> list[dict[str, Any]]:
    blob = text_blob(job)
    scored: list[tuple[int, dict[str, Any]]] = []
    for project in load_portfolio():
        hits = sum(1 for kw in project.get("keywords", []) if normalize(kw) in blob)
        if project["id"] in {"ghx", "n8n", "airtable", "voice"} and any(
            k in blob for k in ["automation", "operations", "workflow", "support", "implementation"]
        ):
            hits += 1
        if hits:
            scored.append(
                (
                    hits,
                    {
                        "id": project["id"],
                        "name": project["name"],
                        "url": project["url"],
                        "blurb": project["blurb"],
                        "metrics": project.get("metrics", []),
                        "match_strength": hits,
                    },
                )
            )
    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored:
        defaults = {p["id"]: p for p in load_portfolio()}
        for pid in ("ghx", "voice", "n8n"):
            p = defaults[pid]
            scored.append(
                (
                    1,
                    {
                        "id": p["id"],
                        "name": p["name"],
                        "url": p["url"],
                        "blurb": p["blurb"],
                        "metrics": p.get("metrics", []),
                        "match_strength": 1,
                    },
                )
            )
    return [item for _, item in scored[:limit]]
