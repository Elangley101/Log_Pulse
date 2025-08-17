import argparse, os, json, random, time, datetime

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--events", type=int, default=10000)
    p.add_argument("--topic", type=str, default="auth.events.v1")
    args = p.parse_args()
    # TODO: actually send to Kafka; for now, write NDJSON to /lake/raw/
    os.makedirs("lake/raw", exist_ok=True)
    path = f"lake/raw/{args.topic.replace('.','_')}.ndjson"
    uas = ["Mozilla/5.0", "Chrome/129", "Safari/17"]
    ips = ["1.2.3.4","5.6.7.8","9.9.9.9","8.8.8.8"]
    with open(path, "w") as f:
        for i in range(args.events):
            event = {
                "ts": datetime.datetime.utcnow().isoformat()+"Z",
                "user_id": f"user_{random.randint(1,50)}",
                "ip": random.choice(ips),
                "user_agent": random.choice(uas),
                "action": "login",
                "result": "fail" if random.random()<0.2 else "success",
            }
            f.write(json.dumps(event)+"\n")
    print(f"Wrote {args.events} events to {path}")

if __name__ == "__main__":
    main()
