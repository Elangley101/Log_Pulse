ROLE: Coder
OBJECTIVE: Implement Milestone-1 exactly as specified by Architect. Ship a reproducible local demo with tests and docs updates. Open PR `feat/m1`.

INPUTS TO LOAD:
- .cursor/rules.md
- docs/MILESTONE-1.md (acceptance criteria)
- docs/HLD.md, docs/NFRs.md, ADR-001/002

DELIVERABLES (match acceptance criteria):
1) Ingestion:
   - `ingestion/synthetic_producer.py` writes NDJSON to lake/raw/auth_events_v1.ndjson (for M1). Read KAFKA_BROKER from env but NDJSON is acceptable fallback.
2) Transform:
   - `transform/run_dbt.py` placeholder now; scaffold dbt project structure; add ≥6 basic tests as soon as models exist.
3) Detection:
   - `detection/rules.py` with brute_force(events, window_minutes=2, threshold=5)
   - `detection/simulate_bruteforce.py` reading the NDJSON and printing offenders
4) Serving:
   - `serving/app.py` (Streamlit stub renders title + two placeholder charts; runs on :8501)
5) Scripts:
   - `scripts/dev_bootstrap.sh` generating 10k events → run transform → simulate detection
6) Tooling:
   - `.env.sample` with KAFKA_BROKER, DUCKDB_PATH, SLACK_WEBHOOK_URL
   - `Makefile` targets work: setup / run / lint / type / test / dbt
   - Dockerfiles for ingestion/detection/serving (basic)
7) Tests:
   - `tests/test_rules.py` covering brute force logic
8) Docs:
   - Ensure README Quickstart works as written
   - Link ADRs from README or HLD

QUALITY GATES:
- `ruff check .` clean
- `mypy .` passes (ignore_missing_imports true is fine)
- `pytest -q` green
- `dbt test` placeholder OK in M1 (models can be added next)
- No secrets committed; `.env.sample` present

PR FLOW:
- Open PR `feat/m1` referencing docs/MILESTONE-1.md
- Include brief PR description with:
  - Commands run and outputs
  - Notes/TODOs for any spec gaps (do not invent new scope; tag Architect)

DON’TS:
- Don’t change scope or acceptance criteria
- Don’t remove docs/tests to “get it to work”
