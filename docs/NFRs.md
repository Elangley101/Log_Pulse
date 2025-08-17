# NFRs (M1)

## Security
- No secrets in repo; use `.env` locally and environment variables in containers.
- Slack webhook stored only in env; never printed in logs.
- Input events contain no sensitive PII beyond `ip`, `user_agent`, and opaque `user_id`.

## Reliability and Operability
- Idempotent transforms; re-running bootstrap or dbt does not create duplicates in curated tables.
- At-least-once event persistence from producer to lake for M1.
- Retries with exponential backoff for transient failures where applicable (M1: minimal, documented).

## Performance
- Handle synthetic rate of ≥1k events/min on a typical developer laptop.
- End-to-end detection latency budget: < 5 seconds.
- Streamlit dashboard initial load < 3 seconds on local warehouse.

## Observability
- Unit tests for rule(s) with `pytest -q` passing.
- dbt tests (≥6 once models exist) passing on curated models.
- Basic logs for each stage (producer, transform, detection, serving).

## Portability
- Local-first; all services containerized or runnable via `make` targets without cloud access.

## Maintainability
- Python 3.11; pinned Python and dbt-duckdb versions in project configuration.
- Clear README quickstart and troubleshooting.
