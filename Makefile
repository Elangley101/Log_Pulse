setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e .[dev]

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
