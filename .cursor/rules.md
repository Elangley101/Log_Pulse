# Shared Rules
- Source of truth: docs/PRD.md, docs/HLD.md, docs/NFRs.md
- Every change updates docs and adds/adjusts tests
- Stack: Python 3.11, Redpanda (Kafka), dbt-core + DuckDB for local demo
- Quality gates: ruff + mypy + pytest + dbt test
- Secrets via .env (never commit real secrets)


