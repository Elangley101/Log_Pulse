from __future__ import annotations
import os
import json
import logging
from typing import Any

import requests


def post_slack_message(text: str, **blocks: Any) -> bool:
    """Post a simple message to Slack webhook if configured.

    Returns True if sent, False if skipped or failed.
    """
    webhook = os.getenv("SLACK_WEBHOOK_URL", "").strip()
    if not webhook:
        logging.info("slack_disabled reason=%s", "no_webhook")
        return False
    payload = {"text": text}
    if blocks:
        payload.update(blocks)
    try:
        resp = requests.post(webhook, data=json.dumps(payload), headers={"Content-Type": "application/json"}, timeout=10)
        if resp.status_code >= 200 and resp.status_code < 300:
            return True
        logging.warning("slack_non_2xx status=%s body=%s", resp.status_code, resp.text)
        return False
    except Exception as exc:  # noqa: BLE001 (simple edge reporting ok)
        logging.error("slack_error error=%s", exc)
        return False
