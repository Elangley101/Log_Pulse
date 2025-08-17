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

## Coder Workload (M1 implementation tasks)
- Implement Slack alerting module:
  - Create `alerting/slack.py` with `post_slack_message(text: str)` using `${SLACK_WEBHOOK_URL}` from env and `requests.post`.
  - Ensure no secrets are logged; handle missing webhook by printing a warning without crashing.
- Align bootstrap output:
  - Update `detection/simulate_bruteforce.py` so bootstrap prints exactly: `Detected brute-force offenders: <comma-separated user_ids>`.
  - Keep Slack posting when offenders exist.
- Add dbt project and tests under `transform/dbt`:
  - Minimal models: stage raw `auth_events` from `lake/raw/auth_events_v1.ndjson` into `stg_auth_events`, then `f_auth_events` curated.
  - Configure DuckDB profile to `${DUCKDB_PATH}`.
  - Add ≥6 tests: not_null (`ts`, `user_id`, `result`), accepted_values (`action` in {login}, `result` in {success,fail}), and uniqueness as appropriate.
  - Ensure `transform/run_dbt.py` completes: deps, seed (if any), run, test.
- Windows support:
  - Add `scripts/dev_bootstrap.ps1` equivalent to `dev_bootstrap.sh` for PowerShell, or clearly document using Git Bash/WSL in `README.md`.
  - Note that `make setup` virtualenv activation path may differ on Windows; document or adjust.
- NDJSON fallback and Kafka:
  - Keep NDJSON writer as default path for M1; optionally add a simple Redpanda producer/consumer behind a flag without blocking M1.
- Update `README.md` Quickstart to reflect the above, including Slack optionality and Windows notes.

## Test Expectations (M1)
- Unit test covers `brute_force` sliding window logic and threshold behavior.
- dbt schema and data tests on curated models (unique keys, not nulls, accepted values) totaling ≥6 once models exist.

## Definition of Done
- All acceptance criteria met on a clean machine following the documented steps in under 10 minutes to first event.
- Reviewer can use this milestone card to validate deliverables end-to-end.
