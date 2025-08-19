from __future__ import annotations
import os
import logging
from typing import List, Tuple

import duckdb


def summarize(offenders: List[Tuple[str, int]]) -> str:
    if not offenders:
        return "No current brute-force offenders."
    top = ", ".join(f"{u}({c})" for u, c in offenders[:5])
    actions = [
        "Block abusive IPs at edge/WAF if repeated across users",
        "Enforce MFA and reset passwords for impacted accounts",
        "Add offenders to watchlist for 24h",
    ]
    return f"Offenders: {top}. Recommended: " + "; ".join(actions) + "."


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if os.getenv("ENABLE_AI_ASSIST", "false").lower() not in {"1", "true", "yes"}:
        logging.info("analyst_disabled reason=%s", "flag_off")
        return

    duckdb_path = os.getenv("DUCKDB_PATH", ".data/logpulse.duckdb")
    con = duckdb.connect(duckdb_path)
    # Aggregate last 30 minutes of failed logins by user
    rows = con.execute(
        """
        SELECT user_id, COUNT(*) AS fails
        FROM stg_auth_events
        WHERE result = 'fail'
          AND ts >= NOW() - INTERVAL 30 MINUTES
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT 50
        """
    ).fetchall()
    offenders = [(r[0], int(r[1])) for r in rows]
    note = summarize(offenders)
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS analyst_recommendations (
          ts TIMESTAMP DEFAULT now(),
          note TEXT
        )
        """
    )
    con.execute("INSERT INTO analyst_recommendations (note) VALUES (?)", [note])
    logging.info("analyst_recommendation_written note=%s", note)


if __name__ == "__main__":
    main()


