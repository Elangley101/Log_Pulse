setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e . && pip install ruff mypy pytest dbt-core duckdb==0.10.3 dbt-duckdb streamlit

lint:
	ruff check .

type:
	mypy .

test:
	pytest -q

dbt:
	dbt test

run:
	docker compose up --build
