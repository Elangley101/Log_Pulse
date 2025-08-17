from collections import defaultdict
from datetime import datetime, timedelta

def brute_force(events, window_minutes=2, threshold=5):
    """
    events: iterable of dicts with keys ts (ISO8601), user_id, result
    Returns list of user_ids exceeding threshold failed logins within window.
    """
    # naive sliding window
    fails = defaultdict(list)
    for e in events:
        if e.get("result") == "fail":
            ts = datetime.fromisoformat(e["ts"].replace("Z","+00:00"))
            fails[e["user_id"]].append(ts)
    offenders = []
    window = timedelta(minutes=window_minutes)
    for user, times in fails.items():
        times.sort()
        left = 0
        for right in range(len(times)):
            while times[right] - times[left] > window:
                left += 1
            if (right - left + 1) >= threshold:
                offenders.append(user)
                break
    return offenders
