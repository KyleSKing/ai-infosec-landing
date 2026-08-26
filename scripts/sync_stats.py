#!/usr/bin/env python3
"""
Sync aggregated stats from Supabase into _data/stats.json so Jekyll
can SSR-inject the values into the homepage sidebar.

Triggered by GitHub Actions after the weekly publish step.
Requires SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY env vars.
"""

import json
import os
import sys
from pathlib import Path

import requests

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
OUT_PATH = Path("_data/stats.json")


def fetch_rpc(name: str, params: dict) -> object:
    if not SUPABASE_URL or not SERVICE_ROLE_KEY:
        raise RuntimeError("SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY not set")
    url = f"{SUPABASE_URL}/rest/v1/rpc/{name}"
    resp = requests.post(
        url,
        headers={
            "apikey": SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
            "content-type": "application/json",
        },
        json=params,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def main() -> int:
    if not SUPABASE_URL or not SERVICE_ROLE_KEY:
        # Not configured — write empty scaffold so templates still render
        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUT_PATH.write_text(
            json.dumps(
                {"top": [], "daily": [], "totals": {}, "synced_at": None},
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print("⚠️  Supabase not configured. Wrote empty stats.json scaffold.")
        return 0

    print("📊 Fetching stats from Supabase...")
    try:
        top = fetch_rpc("top_articles", {"days": 7, "lim": 5})
        daily = fetch_rpc("daily_stats", {"days": 30})
        totals_rows = fetch_rpc("site_totals", {})
        totals = totals_rows[0] if totals_rows else {}
    except Exception as exc:
        print(f"❌ Failed to fetch stats: {exc}")
        return 1

    payload = {
        "top": top or [],
        "daily": daily or [],
        "totals": {
            "total_pv": int(totals.get("total_pv") or 0),
            "total_uv": int(totals.get("total_uv") or 0),
            "total_likes": int(totals.get("total_likes") or 0),
            "total_articles": int(totals.get("total_articles") or 0),
        },
        "synced_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(
        f"✅ Wrote {OUT_PATH}: top={len(payload['top'])}, "
        f"daily={len(payload['daily'])}, "
        f"totals={payload['totals']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
