# LogPulse (SIEM-lite)
Cloud-native security data platform: log ingestion → enrichment → detection (rules + anomalies) → dashboard → alerts.

## Modules
- ingestion (Kafka/Redpanda producers & consumer)
- transform (dbt + DuckDB locally)
- detection (rule engine + anomaly later)
- serving (Streamlit dashboard)
- alerting (Slack webhook)
- observability (tests, lineage, health)
- infra (Terraform later, Docker now)

## Quickstart
1) `make setup`
2) Copy `.env.sample` → `.env` and fill SLACK_WEBHOOK_URL (optional).
3) `make run`
4) `bash scripts/dev_bootstrap.sh` (use Git Bash/WSL on Windows) or `powershell -ExecutionPolicy Bypass -File scripts/dev_bootstrap.ps1`

### Windows-friendly commands (PowerShell)
```powershell
# setup venv + deps
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install "dbt-core==1.10.*" "dbt-duckdb==1.10.*" ruff mypy pytest streamlit duckdb==0.10.3

# env
Copy-Item .env.sample .env -Force

# generate → transform → detect
$env:DUCKDB_PATH = '.data/logpulse.duckdb'
.\.venv\Scripts\python.exe ingestion\synthetic_producer.py --events 10000 --topic auth.events.v1
.\.venv\Scripts\python.exe transform\run_dbt.py
.\.venv\Scripts\python.exe detection\simulate_bruteforce.py --user demo --ip 1.2.3.4

# or run one command
powershell -ExecutionPolicy Bypass -File scripts\dev_bootstrap.ps1

# tests / lint / type
.\.venv\Scripts\pytest -q
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy .

# dashboard
streamlit run serving/app.py --server.port=8501
```


