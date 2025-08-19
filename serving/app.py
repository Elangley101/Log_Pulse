import os
import streamlit as st
import duckdb

st.title("LogPulse")

duckdb_path = os.getenv("DUCKDB_PATH", ".data/logpulse.duckdb")
try:
    con = duckdb.connect(duckdb_path, read_only=True)
    # Aggregates by result
    result_rows = con.execute(
        """
        SELECT result, COUNT(*) AS cnt
        FROM stg_auth_events
        GROUP BY 1
        ORDER BY 2 DESC
        """
    ).fetchall()
    by_result = {r[0] or "unknown": r[1] for r in result_rows}

    # Top failed users
    top_failed_rows = con.execute(
        """
        SELECT user_id, COUNT(*) AS fails
        FROM stg_auth_events
        WHERE result = 'fail'
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT 10
        """
    ).fetchall()
    top_users = {r[0]: r[1] for r in top_failed_rows}

    st.subheader("Events by result")
    st.bar_chart({"count": by_result})

    st.subheader("Top failed login users")
    st.bar_chart({"count": top_users})

    st.subheader("Rule detections (recent runs)")
    logs = con.execute(
        """
        SELECT * FROM (
            SELECT 'brute_force' AS rule, COUNT(*) AS cnt FROM alerts WHERE message LIKE 'brute_force%'
            UNION ALL
            SELECT 'impossible_travel' AS rule, COUNT(*) FROM alerts WHERE message LIKE 'impossible_travel%'
            UNION ALL
            SELECT 'password_spray' AS rule, COUNT(*) FROM alerts WHERE message LIKE 'password_spray%'
        )
        """
    ).fetchall()
    rule_counts = {r[0]: r[1] for r in logs}
    st.bar_chart({"count": rule_counts})

    st.subheader("Events timeline (last 1h)")
    ts_rows = con.execute(
        """
        SELECT DATE_TRUNC('minute', ts) as minute, COUNT(*) AS cnt
        FROM stg_auth_events
        WHERE ts >= NOW() - INTERVAL 1 HOUR
        GROUP BY 1
        ORDER BY 1
        """
    ).fetchall()
    timeline = {str(r[0]): r[1] for r in ts_rows}
    if timeline:
        st.line_chart({"count": timeline})

    st.subheader("Recent alerts (last 50)")
    try:
        alerts = con.execute(
            """
            SELECT ts, message
            FROM alerts
            ORDER BY ts DESC
            LIMIT 50
            """
        ).fetchall()
        if alerts:
            st.table({"ts": [str(a[0]) for a in alerts], "message": [a[1] for a in alerts]})
        else:
            st.info("No alerts yet.")
    except Exception:
        st.info("Alerts table not present yet.")

    st.subheader("Analyst recommendations (last 10)")
    try:
        recs = con.execute(
            """
            SELECT ts, note
            FROM analyst_recommendations
            ORDER BY ts DESC
            LIMIT 10
            """
        ).fetchall()
        if recs:
            st.table({"ts": [str(r[0]) for r in recs], "note": [r[1] for r in recs]})
        else:
            st.info("No recommendations yet.")
    except Exception:
        st.info("Recommendations table not present yet.")

    st.success("Dashboard running against DuckDB")
except Exception as exc:
    st.error(f"Failed to read from DuckDB at {duckdb_path}: {exc}")
    st.info("Run the bootstrap script to generate and transform events.")
