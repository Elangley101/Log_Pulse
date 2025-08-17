from __future__ import annotations
import os
import json
from typing import Any

import requests


def post_slack_message(text: str, **blocks: Any) -> bool:
    """Post a simple message to Slack webhook if configured.

    Returns True if sent, False if skipped or failed.
    """
    webhook = os.getenv("SLACK_WEBHOOK_URL", "").strip()
    if not webhook:
        # No webhook configured; skip silently and return False
        print("[slack] SLACK_WEBHOOK_URL not set; skipping alert")
        return False
    payload = {"text": text}
    if blocks:
        payload.update(blocks)
    try:
        resp = requests.post(webhook, data=json.dumps(payload), headers={"Content-Type": "application/json"}, timeout=10)
        if resp.status_code >= 200 and resp.status_code < 300:
            return True
        print(f"[slack] webhook responded {resp.status_code}: {resp.text}")
        return False
    except Exception as exc:  # noqa: BLE001 (simple edge reporting ok)
        print(f"[slack] error sending alert: {exc}")
        return False
