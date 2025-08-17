# Milestone Card: M1 Local Demo
Scope: local only; Redpanda + DuckDB + dbt (stub) + Streamlit + Slack.

Interfaces/Env:
- Topic: auth.events.v1 (JSON)
- Files: lake/raw/auth_events_v1.ndjson ; lake/parquet/... (later)
- dbt target: duckdb (to be initialized)
- Detection API (internal): brute_force(events, window=2m, threshold=5)
- Env: KAFKA_BROKER, DUCKDB_PATH, SLACK_WEBHOOK_URL

Acceptance:
- `make setup` completes
- `make run` starts services
- `bash scripts/dev_bootstrap.sh` writes 10k events and prints offenders
- `pytest -q` passes (>=1 test)
- Streamlit runs on :8501 and renders stub
- Docs exist (PRD, HLD, NFRs, ADR template)
- `.env.sample` present

Docs:
- Update HLD with mermaid (done), keep PRD/NFRs aligned.
- ADRs to add in PR: 001-warehouse (DuckDB), 002-queue (Redpanda).
