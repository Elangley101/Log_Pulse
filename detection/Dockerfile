FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install -U pip && pip install requests==2.32.* duckdb==1.1.*
ENV BRUTE_WINDOW_MIN=2 BRUTE_THRESHOLD=5 IMPOSSIBLE_TRAVEL_WINDOW_MIN=15 SPRAY_WINDOW_MIN=5 SPRAY_MIN_USERS=10 SPRAY_MAX_ATTEMPTS_PER_USER=3
CMD ["python","simulate_bruteforce.py","--loop","--interval-seconds","15"]
