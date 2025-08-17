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
4) `bash scripts/dev_bootstrap.sh`


