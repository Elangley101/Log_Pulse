# Seeds
No seeds required for M1; placeholder to satisfy dbt structure.

This project persists rule outputs into DuckDB tables `alerts` and `analyst_recommendations` at runtime. If you prefer dbt-managed DDL, add models for those tables under `models/` and remove the app-side CREATE TABLE statements.