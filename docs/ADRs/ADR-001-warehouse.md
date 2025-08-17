# ADR-001: Local Warehouse is DuckDB
## Context
For a local, low-friction demo and development workflow, we need an embedded analytical database with minimal setup and strong SQL and columnar performance.

## Decision
Adopt DuckDB as the local warehouse for M1. dbt-duckdb will be used for modeling and tests.

## Consequences
- Pros: zero external dependency, fast columnar analytics, easy file I/O (Parquet/CSV/NDJSON via staging), great for CI/local.
- Cons: single-file DB, no concurrent writer support for multi-service writes; future scale requires migration.

## Alternatives
- SQLite: poor for analytics; limited columnar performance.
- Postgres: heavier local setup; great general-purpose but more ops.
- BigQuery/Snowflake: not local-friendly; cost and credentials overhead.
