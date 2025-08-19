FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install -U pip && pip install duckdb==1.1.*
CMD ["python","service.py"]


