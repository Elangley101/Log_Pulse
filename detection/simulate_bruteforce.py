import argparse, json

from rules import brute_force

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--user", default="demo")
    p.add_argument("--ip", default="1.2.3.4")
    args = p.parse_args()
    # minimal sample
    with open("lake/raw/auth_events_v1.ndjson","r") as f:
        lines = [json.loads(x) for x in f.readlines()[:10000]]
    offenders = brute_force(lines, window_minutes=2, threshold=5)
    print("Offenders:", offenders)

if __name__ == "__main__":
    main()
