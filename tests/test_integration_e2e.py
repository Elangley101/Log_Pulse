import os
from pathlib import Path

import duckdb

from detection.simulate_bruteforce import detect_once


def test_e2e_bootstrap_and_detect(tmp_path: Path) -> None:
    # Prepare DuckDB
    db_path = tmp_path / "logpulse.duckdb"
    con = duckdb.connect(str(db_path))
    # Create staging table from sample NDJSON
    sample_path = tmp_path / "auth_events_v1.ndjson"
    lines = [
        '{"ts":"2025-01-01T00:00:00Z","user_id":"user_1","result":"fail"}',
        '{"ts":"2025-01-01T00:00:20Z","user_id":"user_1","result":"fail"}',
        '{"ts":"2025-01-01T00:00:40Z","user_id":"user_1","result":"fail"}',
        '{"ts":"2025-01-01T00:01:00Z","user_id":"user_1","result":"fail"}',
        '{"ts":"2025-01-01T00:01:20Z","user_id":"user_1","result":"fail"}',
        '{"ts":"2025-01-01T00:01:40Z","user_id":"user_2","result":"success"}',
    ]
    sample_path.write_text("\n".join(lines), encoding="utf-8")
    con.execute(
        f"""
        CREATE OR REPLACE VIEW stg_auth_events AS
        SELECT * FROM read_json_auto('{sample_path.as_posix()}')
        """
    )
    con.close()

    offenders = detect_once(str(db_path), window_minutes=2, threshold=5)
    assert "user_1" in offenders

    # Alerts table should have at least one row
    con = duckdb.connect(str(db_path))
    rows = con.execute("SELECT COUNT(*) FROM alerts").fetchone()
    assert rows and rows[0] >= 1
    con.close()


