import json
import os
import time
import logging
from pathlib import Path
from typing import Optional

try:
    from kafka import KafkaConsumer  # type: ignore
except Exception:
    KafkaConsumer = None


def main() -> None:
    broker: Optional[str] = os.getenv("KAFKA_BROKER")
    topic: str = os.getenv("KAFKA_TOPIC", "auth.events.v1")
    if not KafkaConsumer:
        logging.warning("consumer_disabled reason=%s", "missing_kafka_client")
        time.sleep(2)
        return

    out_dir = Path("lake/raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{topic.replace('.', '_')}.ndjson"

    # Exponential backoff for broker readiness
    backoff = 1.0
    max_backoff = 30.0
    consumer = None
    while True:
        if not broker:
            logging.warning("consumer_waiting reason=%s", "no_broker_env")
            time.sleep(min(backoff, max_backoff))
            backoff = min(max_backoff, backoff * 2)
            broker = os.getenv("KAFKA_BROKER")
            continue
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=broker,
                enable_auto_commit=True,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
                consumer_timeout_ms=30000,
            )
            logging.info("consumer_connected broker=%s topic=%s", broker, topic)
            break
        except Exception as exc:  # noqa: BLE001
            logging.warning("consumer_connect_retry error=%s backoff=%.1fs", exc, backoff)
            time.sleep(backoff)
            backoff = min(max_backoff, backoff * 2)

    messages_written = 0
    logging.info("consumer_started topic=%s out=%s", topic, out_path)
    while True:
        try:
            with out_path.open("a", encoding="utf-8") as f:
                for msg in consumer:  # type: ignore[arg-type]
                    f.write(json.dumps(msg.value) + "\n")
                    messages_written += 1
                    if messages_written % 1000 == 0:
                        logging.info("consumer_progress written=%d", messages_written)
        except Exception as exc:  # noqa: BLE001
            logging.error("consumer_stream_error error=%s", exc)
            time.sleep(2)
            try:
                consumer.close()  # type: ignore[union-attr]
            except Exception:
                pass
            # Attempt reconnect
            backoff = 1.0
            while True:
                try:
                    consumer = KafkaConsumer(
                        topic,
                        bootstrap_servers=broker,  # type: ignore[arg-type]
                        enable_auto_commit=True,
                        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                        auto_offset_reset="earliest",
                        consumer_timeout_ms=30000,
                    )
                    logging.info("consumer_reconnected")
                    break
                except Exception as exc2:  # noqa: BLE001
                    logging.warning("consumer_reconnect_retry error=%s backoff=%.1fs", exc2, backoff)
                    time.sleep(backoff)
                    backoff = min(max_backoff, backoff * 2)


if __name__ == "__main__":
    main()


