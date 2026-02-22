/* @bruin
name: staging.trips
type: duckdb.sql

depends:
  - ingestion.trips
  - ingestion.payment_lookup

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
  time_granularity: timestamp

columns:
  - name: pickup_datetime
    type: timestamp
    description: When the trip started
    primary_key: true
    nullable: false
    checks:
      - name: not_null
  - name: dropoff_datetime
    type: timestamp
    description: When the trip ended
    checks:
      - name: not_null
  - name: taxi_type
    type: string
    description: Source taxi type (yellow, green)
    checks:
      - name: not_null

custom_checks:
  - name: row_count_positive
    description: Ensures the table is not empty after a run
    query: |
      SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END FROM staging.trips
    value: 1
@bruin */

SELECT *
FROM ingestion.trips
WHERE pickup_datetime >= '{{ start_datetime }}'
  AND pickup_datetime < '{{ end_datetime }}'
