FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install -U pip && pip install requests
CMD ["python","simulate_bruteforce.py","--user","demo","--ip","1.2.3.4"]
