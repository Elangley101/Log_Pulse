{{ config(materialized='table') }}

-- Empty table for app to insert alerts into
SELECT
  CAST(NULL AS TIMESTAMP) AS ts,
  CAST(NULL AS VARCHAR) AS message
WHERE 1=0


