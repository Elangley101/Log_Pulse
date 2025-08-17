param(
  [int]$Events = 10000,
  [string]$Topic = "auth.events.v1",
  [string]$User = "demo",
  [string]$Ip = "1.2.3.4"
)

$ErrorActionPreference = 'Stop'

$python = ".\.venv\Scripts\python.exe"

& $python ingestion\synthetic_producer.py --events $Events --topic $Topic
& $python transform\run_dbt.py
& $python detection\simulate_bruteforce.py --user $User --ip $Ip
