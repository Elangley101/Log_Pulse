FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install -U pip && pip install pydantic requests
CMD ["python","synthetic_producer.py","--events","1000","--topic","auth.events.v1"]
