{{ config(materialized='view') }}

WITH raw AS (
  SELECT *
  FROM read_json_auto('../../lake/raw/auth_events_v1.ndjson')
)
SELECT
  ts,
  user_id,
  ip,
  user_agent,
  action,
  result
FROM raw
