from detection.rules import brute_force
from datetime import datetime, timedelta

def iso(dt): return dt.isoformat()+"Z"

def test_bruteforce_detects_user():
    base = datetime(2024,1,1,0,0,0)
    events = []
    # 5 fails in 2 minutes for user_1
    for i in range(5):
        events.append({"ts": iso(base + timedelta(seconds=20*i)), "user_id": "user_1", "result": "fail"})
    # some successes/noise
    events.append({"ts": iso(base), "user_id": "user_2", "result": "success"})
    offenders = brute_force(events, window_minutes=2, threshold=5)
    assert "user_1" in offenders
