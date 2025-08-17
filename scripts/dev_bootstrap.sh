#!/usr/bin/env bash
set -e
python ingestion/synthetic_producer.py --events 10000 --topic auth.events.v1
python transform/run_dbt.py
python detection/simulate_bruteforce.py --user demo --ip 1.2.3.4
