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


def impossible_travel(events, window_minutes=15, min_ip_change_octet=1):
    """
    Heuristic: flag users with two login attempts within window from sufficiently different IPs.
    No geo; uses change in first N octets as a proxy for distant networks.

    events: iterable of dicts with keys ts (ISO8601), user_id, ip
    """
    window = timedelta(minutes=window_minutes)
    user_to_events = defaultdict(list)
    for e in events:
        if e.get("action", "login") != "login":
            continue
        if not e.get("ip") or not e.get("user_id") or not e.get("ts"):
            continue
        try:
            ts = datetime.fromisoformat(e["ts"].replace("Z","+00:00"))
        except Exception:
            continue
        user_to_events[e["user_id"]].append((ts, e["ip"]))
    offenders: list[str] = []
    for user, rows in user_to_events.items():
        rows.sort(key=lambda r: r[0])
        left = 0
        for right in range(len(rows)):
            while rows[right][0] - rows[left][0] > window:
                left += 1
            # check any pair in window for IP octet distance
            _, ip_r = rows[right]
            ip_r_parts = ip_r.split(".")
            for i in range(left, right):
                _, ip_l = rows[i]
                ip_l_parts = ip_l.split(".")
                if len(ip_r_parts) == 4 and len(ip_l_parts) == 4:
                    # compare up to min_ip_change_octet octets from start
                    if any(ip_r_parts[k] != ip_l_parts[k] for k in range(min_ip_change_octet)):
                        offenders.append(user)
                        break
            if user in offenders:
                break
    return offenders


def password_spray(
    events,
    window_minutes: int = 5,
    min_distinct_users: int = 10,
    max_attempts_per_user: int = 3,
):
    """
    Identify IPs with failed login attempts across many distinct users in a short window,
    while each user sees only a few attempts (spray heuristic).
    Returns list of offender IPs.
    """
    window = timedelta(minutes=window_minutes)
    ip_to_events: dict[str, list[tuple[datetime, str]]] = defaultdict(list)
    for e in events:
        if e.get("result") != "fail":
            continue
        ip = e.get("ip")
        user = e.get("user_id")
        ts_raw = e.get("ts")
        if not ip or not user or not ts_raw:
            continue
        try:
            ts = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
        except Exception:
            continue
        ip_to_events[ip].append((ts, user))

    offenders: list[str] = []
    for ip, rows in ip_to_events.items():
        rows.sort(key=lambda x: x[0])
        left = 0
        user_counts: dict[str, int] = defaultdict(int)
        distinct_users_in_window = 0
        seen_users_in_window: dict[str, int] = defaultdict(int)
        for right in range(len(rows)):
            ts_r, user_r = rows[right]
            seen_users_in_window[user_r] += 1
            while ts_r - rows[left][0] > window:
                user_l = rows[left][1]
                seen_users_in_window[user_l] -= 1
                if seen_users_in_window[user_l] == 0:
                    del seen_users_in_window[user_l]
                left += 1
            # Evaluate window
            distinct = len(seen_users_in_window)
            if distinct >= min_distinct_users and all(c <= max_attempts_per_user for c in seen_users_in_window.values()):
                offenders.append(ip)
                break
    return offenders