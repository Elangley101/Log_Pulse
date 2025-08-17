# PRD: LogPulse SIEM-lite
## Problem
Small teams need low-cost detection on auth/web logs with clear alerts.

## Goals (MVP)
- Ingest synthetic auth/web logs (≥1k events/min local).
- Enrich with geoIP + user-agent.
- Rule detections: brute force, impossible travel, privilege escalation.
- Streamlit dashboard: events timeline, top offenders, alerts feed.
- Slack alerts on critical rules.
- Local deploy via docker-compose.

## V1 (Next)
- Anomaly detection (unsupervised).
- Terraform deploy to Azure.

## Non-Goals
- Full SOC workflows, SOAR playbooks.

## Success Metrics
- <10 min setup to first event.
- <5 sec detection latency on local stack.
- >95% rule test pass rate.


