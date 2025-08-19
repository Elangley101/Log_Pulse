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
2) Create a `.env` file (see below) and fill `SLACK_WEBHOOK_URL` (optional) and `DUCKDB_PATH`.
3) `make run`
4) `bash scripts/dev_bootstrap.sh` (use Git Bash/WSL on Windows) or `powershell -ExecutionPolicy Bypass -File scripts/dev_bootstrap.ps1`

### Windows-friendly commands (PowerShell)
```powershell
# setup venv + deps
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install "dbt-core==1.10.*" "dbt-duckdb==1.10.*" ruff mypy pytest streamlit duckdb==1.1.*

# env
@"
DUCKDB_PATH=.data/logpulse.duckdb
SLACK_WEBHOOK_URL=
KAFKA_BROKER=localhost:9092
STREAMLIT_PORT=8501
BRUTE_WINDOW_MIN=2
BRUTE_THRESHOLD=5
IMPOSSIBLE_TRAVEL_WINDOW_MIN=15
SPRAY_WINDOW_MIN=5
SPRAY_MIN_USERS=10
SPRAY_MAX_ATTEMPTS_PER_USER=3
"@ | Set-Content .env -Encoding UTF8

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

# dashboard against DuckDB
streamlit run serving/app.py --server.port=8501
```

## Analyst service (optional)
- Set `ENABLE_AI_ASSIST=true` in `.env` to enable the analyst service.
- It summarizes recent brute-force activity and writes recommendations to DuckDB (`analyst_recommendations`).
- Recommendations and recent alerts are visible in the Streamlit dashboard.


