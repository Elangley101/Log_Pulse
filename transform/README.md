# transform
Holds dbt project for staging + curated models on DuckDB.

Service runs `run_dbt.py` to materialize models into the DuckDB file at `DUCKDB_PATH`.