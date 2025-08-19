import argparse
import os
import logging
import time
from datetime import datetime, timezone
import duckdb
from detection.rules import brute_force, impossible_travel, password_spray
from alerting.slack import post_slack_message


def detect_once(duckdb_path: str, window_minutes: int, threshold: int) -> list[str]:
    """Run detection once against DuckDB and persist alerts if any.

    Returns list of offender user_ids.
    """
    con = duckdb.connect(duckdb_path, read_only=False)
    rows = con.execute(
        """
        SELECT ts, user_id, result
        FROM stg_auth_events
        ORDER BY ts DESC
        LIMIT 100000
        """
    ).fetchall()
    events: list[dict] = []
    for ts_val, user_id, result in rows:
        if isinstance(ts_val, datetime):
            ts_iso = ts_val.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
        else:
            ts_iso = str(ts_val)
        events.append({"ts": ts_iso, "user_id": user_id, "result": result})
    offenders = brute_force(events, window_minutes=window_minutes, threshold=threshold)
    if offenders:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
              ts TIMESTAMP DEFAULT now(),
              message TEXT
            )
            """
        )
        con.execute(
            "INSERT INTO alerts (message) VALUES (?)",
            [f"brute_force offenders: {', '.join(offenders)}"],
        )
    con.close()
    return offenders


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--user", default="demo")
    p.add_argument("--ip", default="1.2.3.4")
    # Allow env overrides for defaults
    p.add_argument("--window-minutes", type=int, default=int(os.getenv("BRUTE_WINDOW_MIN", "2")))
    p.add_argument("--threshold", type=int, default=int(os.getenv("BRUTE_THRESHOLD", "5")))
    p.add_argument("--loop", action="store_true")
    p.add_argument("--interval-seconds", type=int, default=15)
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    duckdb_path = os.getenv("DUCKDB_PATH", ".data/logpulse.duckdb")

    def run_once() -> None:
        start = time.time()
        offenders = detect_once(
            duckdb_path=duckdb_path,
            window_minutes=args.window_minutes,
            threshold=args.threshold,
        )
        logging.info("detected_offenders rule=brute_force count=%d offenders=%s", len(offenders), offenders)
        # Evaluate other rules and persist alerts as well
        try:
            con = duckdb.connect(duckdb_path, read_only=False)
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS alerts (
                  ts TIMESTAMP DEFAULT now(),
                  message TEXT
                )
                """
            )

            # Impossible travel on recent successes
            try:
                rows2 = con.execute(
                    """
                    SELECT ts, user_id, ip, 'login' as action
                    FROM stg_auth_events
                    WHERE result = 'success'
                    ORDER BY ts DESC
                    LIMIT 200000
                    """
                ).fetchall()
                ev2 = [{"ts": str(r[0]), "user_id": r[1], "ip": r[2], "action": "login"} for r in rows2]
                it_offenders = impossible_travel(
                    ev2,
                    window_minutes=int(os.getenv("IMPOSSIBLE_TRAVEL_WINDOW_MIN", "15")),
                    min_ip_change_octet=1,
                )
                if it_offenders:
                    logging.info(
                        "detected_offenders rule=impossible_travel count=%d offenders=%s",
                        len(it_offenders),
                        it_offenders,
                    )
                    con.execute(
                        "INSERT INTO alerts (message) VALUES (?)",
                        [f"impossible_travel offenders: {', '.join(it_offenders)}"],
                    )
            except Exception as exc:
                logging.warning("impossible_travel_eval_failed error=%s", exc)

            # Password spray on recent failures
            try:
                rows3 = con.execute(
                    """
                    SELECT ts, user_id, ip, result
                    FROM stg_auth_events
                    WHERE result = 'fail'
                    ORDER BY ts DESC
                    LIMIT 200000
                    """
                ).fetchall()
                ev3 = [{"ts": str(r[0]), "user_id": r[1], "ip": r[2], "result": r[3]} for r in rows3]
                spray_offenders = password_spray(
                    ev3,
                    window_minutes=int(os.getenv("SPRAY_WINDOW_MIN", "5")),
                    min_distinct_users=int(os.getenv("SPRAY_MIN_USERS", "10")),
                    max_attempts_per_user=int(os.getenv("SPRAY_MAX_ATTEMPTS_PER_USER", "3")),
                )
                if spray_offenders:
                    logging.info(
                        "detected_offenders rule=password_spray count=%d offenders=%s",
                        len(spray_offenders),
                        spray_offenders,
                    )
                    con.execute(
                        "INSERT INTO alerts (message) VALUES (?)",
                        [f"password_spray offenders: {', '.join(spray_offenders)}"],
                    )
            except Exception as exc:
                logging.warning("password_spray_eval_failed error=%s", exc)
            finally:
                con.close()
        except Exception as exc:
            logging.warning("detection_persist_failed error=%s", exc)
        if offenders:
            post_slack_message(text=f"LogPulse: brute force offenders detected: {', '.join(offenders)}")
        logging.info("detection_latency_ms=%d", int((time.time() - start) * 1000))

    if args.loop:
        logging.info("starting detection loop interval=%ss", args.interval_seconds)
        while True:
            try:
                run_once()
            except Exception as exc:
                logging.error("detection_error error=%s", exc)
            time.sleep(max(1, args.interval_seconds))
    else:
        run_once()


if __name__ == "__main__":
    main()
