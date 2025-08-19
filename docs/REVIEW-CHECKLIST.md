- [ ] Matches M1 scope (local demo only)
- [ ] README quickstart works end-to-end
- [ ] `make setup` ok; `make run` ok; `bash scripts/dev_bootstrap.sh` ok
- [ ] `pytest` passes; dbt placeholder present
- [ ] No secrets committed; `.env.sample` present
- [ ] ADRs added: 001 warehouse, 002 queue
- [ ] Streamlit accessible on 8501

Implementation specifics (M1):
- [ ] Slack alerting: `alerting/slack.py` exists; uses `SLACK_WEBHOOK_URL`; no secrets logged
- [ ] Bootstrap prints exactly: `Detected brute-force offenders: ...`
- [ ] dbt project present under `transform/dbt`; `dbt run` and `dbt test` succeed
- [ ] dbt has ≥6 tests (not_null, accepted_values, uniqueness where applicable)
- [ ] Windows support: `scripts/dev_bootstrap.ps1` exists or README documents Git Bash/WSL path
- [ ] NDJSON fallback works; Kafka optional and documented
Production-ready (baseline):
- [ ] All runtime deps pinned in `pyproject.toml`; Dockerfiles install via `pip install .`
- [ ] Dashboard and detection read from DuckDB, not raw NDJSON
- [ ] `transform` service present; Compose dependency chain correct
- [ ] `.env.sample` exists and is referenced in docs
- [ ] CI runs ruff, mypy, pytest, dbt run/test on PRs
- [ ] Healthchecks or basic start-up validation for services