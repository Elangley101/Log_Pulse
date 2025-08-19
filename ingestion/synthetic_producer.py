import argparse, os, json, random, datetime, time, logging
from typing import Optional

try:
    from kafka import KafkaProducer  # type: ignore
except Exception:  # pragma: no cover
    KafkaProducer = None  # fallback when kafka-python not installed

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--events", type=int, default=10000)
    p.add_argument("--topic", type=str, default="auth.events.v1")
    p.add_argument("--rate", type=int, default=0, help="events per second (0 = burst)")
    args = p.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    # Write NDJSON to /lake/raw/
    os.makedirs("lake/raw", exist_ok=True)
    path = f"lake/raw/{args.topic.replace('.','_')}.ndjson"
    uas = ["Mozilla/5.0", "Chrome/129", "Safari/17"]
    ips = ["1.2.3.4","5.6.7.8","9.9.9.9","8.8.8.8"]
    with open(path, "w", encoding="utf-8") as f:
        for i in range(args.events):
            event = {
                "ts": datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
                "user_id": f"user_{random.randint(1,50)}",
                "ip": random.choice(ips),
                "user_agent": random.choice(uas),
                "action": "login",
                "result": "fail" if random.random()<0.2 else "success",
            }
            line = json.dumps(event)
            f.write(line+"\n")
            # Optionally publish to Kafka if broker configured
            # Lazily initialize producer
            # This is best-effort; failure prints and continues writing NDJSON
            broker: Optional[str] = os.getenv("KAFKA_BROKER")
            if broker and KafkaProducer:
                try:
                    if not hasattr(main, "_producer"):
                        main._producer = KafkaProducer(bootstrap_servers=broker, value_serializer=lambda v: json.dumps(v).encode("utf-8"))
                    main._producer.send(args.topic, value=event)
                except Exception as exc:  # noqa: BLE001
                    logging.warning("kafka_publish_failed error=%s", exc)
            if args.rate and (i % max(1, args.rate) == 0):
                time.sleep(1)
    logging.info("producer_complete events=%d path=%s", args.events, path)

if __name__ == "__main__":
    main()
