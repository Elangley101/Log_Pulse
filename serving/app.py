import json
from collections import Counter
from pathlib import Path

import streamlit as st

st.title("LogPulse")

ndjson_path = Path("lake/raw/auth_events_v1.ndjson")
if ndjson_path.exists():
    with ndjson_path.open("r") as f:
        rows = [json.loads(x) for x in f.readlines()[:5000]]
    st.write(f"Loaded {len(rows)} events from {ndjson_path}")
    by_result = Counter(r.get("result", "unknown") for r in rows)
    by_user_fail = Counter(r["user_id"] for r in rows if r.get("result") == "fail")

    st.subheader("Events by result")
    st.bar_chart({"count": by_result})

    st.subheader("Top failed login users")
    top_users = dict(by_user_fail.most_common(10))
    st.bar_chart({"count": top_users})
else:
    st.info("No data yet. Run the bootstrap script to generate events.")

st.success("Dashboard stub is running.")
