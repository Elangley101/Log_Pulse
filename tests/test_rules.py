from detection.rules import brute_force, impossible_travel, password_spray
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


def test_impossible_travel_detects_user():
    base = datetime(2024,1,1,0,0,0)
    events = []
    # same user, two quick logins from sufficiently different IP blocks
    events.append({"ts": iso(base), "user_id": "user_A", "ip": "1.2.3.4", "action": "login"})
    events.append({"ts": iso(base + timedelta(minutes=1)), "user_id": "user_A", "ip": "9.8.7.6", "action": "login"})
    offenders = impossible_travel(events, window_minutes=15, min_ip_change_octet=1)
    assert "user_A" in offenders


def test_password_spray_detects_ip():
    base = datetime(2024, 1, 1, 0, 0, 0)
    events = []
    # IP 9.9.9.9 fails 10 different users once each within 5 minutes
    for i in range(10):
        events.append({
            "ts": iso(base + timedelta(seconds=20*i)),
            "user_id": f"user_{i}",
            "ip": "9.9.9.9",
            "result": "fail",
            "action": "login",
        })
    offenders = password_spray(events, window_minutes=5, min_distinct_users=10, max_attempts_per_user=1)
    assert "9.9.9.9" in offenders
