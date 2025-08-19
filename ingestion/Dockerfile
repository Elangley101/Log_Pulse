FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install -U pip && pip install kafka-python==2.0.2 requests==2.32.*
ENV KAFKA_TOPIC=auth.events.v1
CMD ["python","consumer.py"]
