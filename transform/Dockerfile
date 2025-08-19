FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install -U pip && pip install dbt-core==1.10.* dbt-duckdb==1.10.* duckdb==1.1.*
CMD ["python","run_dbt.py"]

