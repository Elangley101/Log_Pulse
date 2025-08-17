# Milestone Card: M1 Local Demo

## Scope
- Local-only pipeline: Redpanda (or NDJSON stub) → NDJSON lake → dbt → DuckDB → detection (brute-force only) → Slack + Streamlit.
- Do not implement additional rules beyond `brute_force` for M1.

## Data Contract
- `auth_log(v1)` fields:
  - `ts` (ISO8601 UTC, `...Z`), `user_id` (string), `ip` (IPv4 string), `user_agent` (string), `action ∈ {login}`, `result ∈ {success,fail}`.
- Transport: Kafka JSON messages or NDJSON lines; one event per message/line.

## Interfaces and Env Vars
- Topic: `auth.events.v1`
- File: `lake/raw/auth_events_v1.ndjson`
- Warehouse/dbt: `${DUCKDB_PATH}`; dbt target configured for DuckDB
- Detection API: `brute_force(events, window_minutes=2, threshold=5) -> list[user_id]`
- Alerts: Slack via `${SLACK_WEBHOOK_URL}`
- Env vars (required unless noted):
  - `KAFKA_BROKER`: e.g., `localhost:19092`
  - `DUCKDB_PATH`: e.g., `./warehouse/logpulse.duckdb`
  - `SLACK_WEBHOOK_URL`: Slack Incoming Webhook
  - `STREAMLIT_PORT` (optional, default `8501`)

## Commands That Must Work
- `make setup`
  - Installs dependencies, prepares local env, validates `.env` presence.
- `make run`
  - Starts Redpanda (if used) and app containers/services; exposes Streamlit on `${STREAMLIT_PORT:-8501}`.
- `bash scripts/dev_bootstrap.sh`
  - Generates ≥10k synthetic auth events into topic/file.
  - Runs dbt to build models into DuckDB.
  - Executes brute-force detection and prints a summary line containing `Detected brute-force offenders:` followed by at least one `user_id`.
- `pytest -q`
  - Runs unit tests (≥1 for rules) and passes.

## Acceptance Criteria
- Running the commands above completes without errors.
- Streamlit accessible at `http://localhost:${STREAMLIT_PORT:-8501}` and shows recent event count and any offenders.
- A Slack message is posted to the configured webhook when offenders are detected during bootstrap.
- dbt tests (≥6 once models exist) pass.
- Documentation exists and is up to date: `docs/PRD.md`, `docs/HLD.md` (with diagrams), `docs/NFRs.md`, ADRs 001 and 002, and `.env.sample`.

## Test Expectations (M1)
- Unit test covers `brute_force` sliding window logic and threshold behavior.
- dbt schema and data tests on curated models (unique keys, not nulls, accepted values) totaling ≥6 once models exist.

## Definition of Done
- All acceptance criteria met on a clean machine following the documented steps in under 10 minutes to first event.
- Reviewer can use this milestone card to validate deliverables end-to-end.
