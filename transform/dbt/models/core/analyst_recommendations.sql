{{ config(materialized='table') }}

-- Empty table for analyst service to insert recommendations into
SELECT
  CAST(NULL AS TIMESTAMP) AS ts,
  CAST(NULL AS VARCHAR) AS note
WHERE 1=0


