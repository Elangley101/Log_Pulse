# PRD: LogPulse SIEM-lite (Milestone 1: Local Demo)

## Problem
Small teams need a low-cost, local-first way to detect risky authentication behavior and surface actionable alerts quickly, without cloud accounts or heavy infrastructure.

## Users
- Security-minded developers and data engineers who want a runnable local demo for auth log detections.
- Early-stage teams validating a minimal SIEM-like pipeline on laptops.

## Scope (M1 only)
- Local-only demo. No cloud services.
- Single rule: brute-force login detection on auth events.
- Data source: synthetic producer writing to Redpanda topic `auth.events.v1` or an NDJSON file `lake/raw/auth_events_v1.ndjson`.
- Warehouse: DuckDB, modeled via dbt-core.
- Dashboard: Streamlit basic views (events count, recent offenders, alerts feed).
- Alerts: Slack webhook for brute-force matches.

## Out of Scope (M1)
- Additional rules (e.g., impossible travel, privilege escalation) beyond placeholders in docs.
- Managed/cloud deployments and IaC.
- Multi-tenant security workflows, ticketing, or SOAR.

## Functional Requirements
- Generate synthetic `auth_log(v1)` events with fields: `ts` (ISO8601 Z), `user_id` (string), `ip` (string IPv4), `user_agent` (string), `action ∈ {login}`, `result ∈ {success,fail}`.
- Persist raw events to `lake/raw/auth_events_v1.ndjson` and/or publish to Redpanda topic `auth.events.v1`.
- Transform data with dbt into curated tables in DuckDB (minimum: `f_auth_events`).
- Detection service exposes a function `brute_force(events, window_minutes=2, threshold=5) -> [user_id]` and produces Slack alerts when offenders are found.
- Streamlit app surfaces recent event counts and any detected offenders.

## Non-Functional Requirements (summarized)
- Local setup in under 10 minutes.
- Deterministic, idempotent transforms; safe re-runs.
- Secret management via `.env` and environment variables only.

## Data Contract: auth_log(v1)
- Schema:
  - `ts`: string (ISO8601 UTC, e.g., `2025-01-01T12:00:00Z`)
  - `user_id`: string (opaque ID)
  - `ip`: string (IPv4 dotted quad)
  - `user_agent`: string
  - `action`: string, allowed values `{login}`
  - `result`: string, allowed values `{success,fail}`
- Transport: Kafka/Redpanda JSON or NDJSON lines; one event per message/line.
- Validation: Events missing required fields are rejected or quarantined (M1 may drop with log warning).

## Success Metrics (M1)
- Time-to-first-event: under 10 minutes from fresh clone using documented commands.
- Local detection latency (producer → detection alert): under 5 seconds at 1k events/min synthetic rate.
- Tests: `pytest -q` passes all included unit tests; dbt tests (≥6 once models exist) pass.
- Slack alert delivered for simulated brute-force scenario during bootstrap script.

## Assumptions & Dependencies
- Python 3.11, Docker/Docker Compose available locally.
- Env vars configured via `.env` or shell: `KAFKA_BROKER`, `DUCKDB_PATH`, `SLACK_WEBHOOK_URL`, optional `STREAMLIT_PORT` (default `8501`). `.env.sample` provided.

## Milestones
- M1 (this PRD): local demo as defined above.
- Later (not in scope): unsupervised anomalies, cloud warehouse, infra-as-code.
