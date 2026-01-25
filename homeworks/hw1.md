# Homework 1 — DataTalksClub Data Engineering Zoomcamp

---

## 🚀 Setup & Execution

### Commands to run containers and complete the homework

```bash
cd /workspaces/data-engineering-zoomcamp-2026/01-docker-terraform/pipeline
```

```bash
docker-compose up -d
```

### Ingest Yellow Taxi Data

```bash
docker run -it \
  --network=pipeline_default \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips_202511 \
    --year=2025 \
    --month=11
```

### Ingest Green Taxi Data

```bash
docker run -it \
  --network=pipeline_default \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=green_taxi_trips_202511 \
    --year=2025 \
    --month=11 \
    --color=green
```

---

## 📘 Questions & Answers

### Question 1 (1 point)

**What’s the version of `pip` in the `python:3.13` image?**

Command used:

```bash
docker run -it --entrypoint=bash python:3.13.1-slim
```

**Answer:** `pip 24.3.1`

---

### Question 2

**Given the `docker-compose.yaml`, what is the hostname and port that pgAdmin should use to connect to Postgres?**

**Answer:** `db:5432`

---

### Question 3

**For the trips in November 2025, how many trips had a `trip_distance` of less than or equal to 1 mile?**

```sql
SELECT
    COUNT(*) AS short_trips_count
FROM
    green_taxi_trips_202511
WHERE
    trip_distance <= 1
    AND lpep_pickup_datetime >= '2025-11-01'
    AND lpep_pickup_datetime < '2025-12-01';
```

**Answer:** `8007`

---

### Question 4

**Which was the pickup day with the longest trip distance?**
*Only consider trips with `trip_distance < 100` miles.*

```sql
SELECT
    DATE(lpep_pickup_datetime) AS pickup_date,
    MAX(trip_distance) AS longest_trip_distance
FROM
    green_taxi_trips_202511
WHERE
    trip_distance < 100
GROUP BY
    DATE(lpep_pickup_datetime)
ORDER BY
    longest_trip_distance DESC
LIMIT 1;
```

**Answer:**

* Date: `2025-11-14`
* Distance: `88.03`

---

### Question 5

**Which was the pickup zone with the largest `total_amount` (sum of all trips) on November 18th, 2025?**

```sql
SELECT
    z."Zone" AS pickup_zone,
    SUM(t.total_amount) AS total_revenue
FROM
    yellow_taxi_trips_202511 t
JOIN
    taxi_zones z
    ON t."PULocationID" = z."LocationID"
WHERE
    DATE(t.tpep_pickup_datetime) = '2025-11-18'
GROUP BY
    z."Zone"
ORDER BY
    total_revenue DESC
LIMIT 1;
```

**Answer:** `East Harlem North`

---

### Question 6

**For passengers picked up in the zone *"East Harlem North"* in November 2025, which drop-off zone had the largest tip?**

```sql
SELECT
    dz."Zone" AS dropoff_zone,
    MAX(t.tip_amount) AS max_tip
FROM
    yellow_taxi_trips_202511 t
JOIN
    taxi_zones pz
    ON t."PULocationID" = pz."LocationID"
JOIN
    taxi_zones dz
    ON t."DOLocationID" = dz."LocationID"
WHERE
    pz."Zone" = 'East Harlem North'
    AND t.tpep_pickup_datetime >= '2025-11-01'
    AND t.tpep_pickup_datetime < '2025-12-01'
GROUP BY
    dz."Zone"
ORDER BY
    max_tip DESC
LIMIT 1;
```

**Answer:**

* Drop-off Zone: `Yorkville West`
* Max Tip: `81.89`

---

### Question 7

**Which sequence describes the Terraform workflow for:**

1. Downloading plugins and setting up the backend
2. Generating and executing changes
3. Removing all resources

**Answer:**

```text
terraform init → terraform apply → terraform destroy
```

---

✅ *Homework completed successfully*
