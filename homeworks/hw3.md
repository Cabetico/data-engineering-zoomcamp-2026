### Question 1. Counting records
What is count of records for the 2024 Yellow Taxi Data?

* 65,623
* 840,402
* 20,332,093
* 85,431,289

the `zoomcamp.yellow_trip_data` is a external table created with the 
Yellow Taxi Trip Records for January 2024 - June 2024

```sql
    SELECT COUNT(*) FROM `zoomcamp.yellow_trip_data`

    output: Row	f0_ 1	20332093
```



A: 20,332,093

### Question 2. Data read estimation
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.

What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

*  18.82 MB for the External Table and 47.60 MB for the Materialized Table
* 0 MB for the External Table and 155.12 MB for the Materialized Table
* 2.14 GB for the External Table and 0MB for the Materialized Table
* 0 MB for the External Table and 0MB for the Materialized Table

```sql
    SELECT COUNT(distinct(PULocationID))
    FROM dtc-de-340821.zoomcamp.yellow_trip_data_materialized;

    SELECT COUNT(distinct(PULocationID))
    FROM dtc-de-340821.zoomcamp.yellow_trip_data;
```
#### Why External Tables Show "0 B" in the Estimate

BigQuery Cannot Pre-Calculate File Sizes for External TablesThe issue:

* External table data lives in GCS, not BigQuery
* BigQuery doesn't automatically scan GCS to determine file sizes
* The query validator doesn't know how large the Parquet files are
* Result: Shows "0 B" as the estimate
* This is a known limitation of external tables!

A: 0 MB for the External Table and 155.12 MB for the Materialized Table

### Question 3. Understanding columnar storage
Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table.

Why are the estimated number of Bytes different?

* BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.
* BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, doubling the estimated bytes processed.
* BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
When selecting multiple columns, 
* BigQuery performs an implicit join operation between them, increasing the estimated bytes processed

A: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

### Question 4. Counting zero fare trips
How many records have a fare_amount of 0?

* 128,210
* 546,578
* 20,188,016
* 8,333


```sql
    SELECT count(*) FROM dtc-de-340821.zoomcamp.yellow_trip_data_materialized WHERE fare_amount = 0;
``` 
A: 8,333


### Question 5. Partitioning and clustering
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)

* Partition by tpep_dropoff_datetime and Cluster on VendorID
* Cluster on by tpep_dropoff_datetime and Cluster on VendorID
* Cluster on tpep_dropoff_datetime Partition by VendorID
* Partition by tpep_dropoff_datetime and Partition by VendorID

In GCP the best practice is to PARTITION(for filtering) columns with high cardinality(dates per exampple) and CLUSTER(for ordering) columns with lower cardinality

A: Partition by tpep_dropoff_datetime and Cluster on VendorID

### Question 6. Partition benefits
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?

Choose the answer which most closely matches.

* 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
* 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table
* 5.87 MB for non-partitioned table and 0 MB for the partitioned table
* 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table

```sql
    SELECT distinct(VendorID)
    FROM `dtc-de-340821.zoomcamp.yellow_trip_data_materialized_partitioned`
    WHERE tpep_dropoff_datetime >= '2024-03-01' and  tpep_dropoff_datetime <= '2024-03-15';

    This query will process 26.84 MB when run.

    SELECT distinct(VendorID)
    FROM dtc-de-340821.zoomcamp.yellow_trip_data_materialized 
    WHERE tpep_dropoff_datetime >= '2024-03-01' and  tpep_dropoff_datetime <= '2024-03-15';

    This query will process 310.24 MB when run.
```
A: 
This query will process 26.84 MB when run and 310.24 MB.

### Question 7. External table storage
Where is the data stored in the External Table you created?

* Big Query
* Container Registry
* GCP Bucket
* Big Table

A: GCP Bucket

### Question 8. Clustering best practices
It is best practice in Big Query to always cluster your data:

* True
* False

#### Why It's FALSE
Clustering is NOT always best practice. It depends on:

1. Table size - Small tables don't benefit from clustering
2. Query patterns - If you don't filter/sort by specific columns, clustering adds no value
3. Data characteristics - High-cardinality unique columns make poor clustering keys
4. Cost vs benefit - Clustering has overhead that may not be worth it


When to CLUSTER
✅ DO Cluster when:

* Table is > 1 GB in size
* You frequently filter by specific columns
* You frequently ORDER BY specific columns
* You use GROUP BY or JOIN on specific columns
* Query patterns are predictable and repetitive
* Column has low to medium cardinality (not unique IDs)

#### When NOT to CLUSTER
❌ DON'T Cluster when:

* Table is < 1 GB (overhead > benefit)
* Ad-hoc queries with unpredictable patterns
* Column is high-cardinality unique (like `trip_id`, `user_id`)
* You **SELECT *** without filters (full table scans anyway)
* Table is rarely queried
* **Write-heavy** workloads (clustering adds overhead on inserts)

#### Real-World Guidelines

| Table Size | Query Pattern | Cluster? | Reasoning |
|------------|---------------|----------|-----------|
| < 1 GB | Any | ❌ No | Table too small - overhead > benefit |
| 1-10 GB | Ad-hoc queries | ❌ No | Unpredictable patterns won't benefit |
| 1-10 GB | Repetitive filters on specific columns | ✅ Yes | Sweet spot for clustering benefits |
| > 10 GB | Ad-hoc queries | 🤔 Maybe | Consider if some common patterns exist |
| > 10 GB | Repetitive filters on specific columns | ✅ Definitely | Large data + predictable queries = maximum benefit |
| > 100 GB | Full table scans (SELECT *) | ❌ No | Clustering won't help full scans |
| > 100 GB | Filters on 2-3 key columns | ✅ Absolutely | Use up to 4 cluster columns for best results |

A: False

### Question 9. Understanding table scans
No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

```sql
    SELECT count(*)
    FROM dtc-de-340821.zoomcamp.yellow_trip_data_materialized;
```

✅ The Answer
`COUNT(*)` doesn't need to read any data columns.
BigQuery stores table metadata that includes the total row count. When you run `COUNT(*)` without WHERE conditions, BigQuery simply reads the metadata instead of scanning the entire table.

```
-- ❌ 0 B processed (reads metadata)
SELECT COUNT(*) 
FROM yellow_trip_data_materialized;

-- ✅ Processes actual bytes (scans column)
SELECT COUNT(VendorID) 
FROM yellow_trip_data_materialized;

-- ✅ Processes actual bytes (scans entire table)
SELECT COUNT(*) 
FROM yellow_trip_data_materialized
WHERE trip_distance > 10;
```