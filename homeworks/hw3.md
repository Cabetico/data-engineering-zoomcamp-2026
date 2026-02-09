# BigQuery Homework - Questions & Answers

## Question 1. Counting Records

**What is count of records for the 2024 Yellow Taxi Data?**

- 65,623
- 840,402
- **20,332,093** ✅
- 85,431,289

### Context
The `zoomcamp.yellow_trip_data` is an external table created with Yellow Taxi Trip Records for January 2024 - June 2024.

### Query
```sql
SELECT COUNT(*) 
FROM `zoomcamp.yellow_trip_data`;
```

### Output
```
Row    f0_
1      20332093
```

**Answer: 20,332,093**

---

## Question 2. Data Read Estimation

**Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?**

- 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- **0 MB for the External Table and 155.12 MB for the Materialized Table** ✅
- 2.14 GB for the External Table and 0MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table

### Queries
```sql
-- Materialized Table
SELECT COUNT(DISTINCT(PULocationID))
FROM `dtc-de-340821.zoomcamp.yellow_trip_data_materialized`;

-- External Table
SELECT COUNT(DISTINCT(PULocationID))
FROM `dtc-de-340821.zoomcamp.yellow_trip_data`;
```

### Why External Tables Show "0 B" in the Estimate

**BigQuery Cannot Pre-Calculate File Sizes for External Tables**

The issue:
- External table data lives in GCS, not BigQuery
- BigQuery doesn't automatically scan GCS to determine file sizes
- The query validator doesn't know how large the Parquet files are
- Result: Shows "0 B" as the estimate
- This is a known limitation of external tables!

**Answer: 0 MB for the External Table and 155.12 MB for the Materialized Table**

---

## Question 3. Understanding Columnar Storage

**Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?**

- **BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.** ✅
- BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, doubling the estimated bytes processed.
- BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
- When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed.

### Explanation

BigQuery uses **columnar storage**, where each column is stored separately. When you query:
- **One column**: Reads only that column's data
- **Two columns**: Reads both columns' data (2× the bytes)

```sql
-- Query 1: Single column
SELECT PULocationID 
FROM table;
-- Processes: Size of PULocationID column

-- Query 2: Two columns
SELECT PULocationID, DOLocationID 
FROM table;
-- Processes: Size of PULocationID + Size of DOLocationID
```

**Answer: BigQuery is a columnar database, and it only scans the specific columns requested in the query.**

---

## Question 4. Counting Zero Fare Trips

**How many records have a fare_amount of 0?**

- 128,210
- 546,578
- 20,188,016
- **8,333** ✅

### Query
```sql
SELECT COUNT(*) 
FROM `dtc-de-340821.zoomcamp.yellow_trip_data_materialized` 
WHERE fare_amount = 0;
```

**Answer: 8,333**

---

## Question 5. Partitioning and Clustering

**What is the best strategy to make an optimized table in BigQuery if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID?**

- **Partition by tpep_dropoff_datetime and Cluster on VendorID** ✅
- Cluster on by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on tpep_dropoff_datetime, Partition by VendorID
- Partition by tpep_dropoff_datetime and Partition by VendorID

### Best Practice Rule

In GCP, the best practice is to:
- **PARTITION** columns with **high cardinality** (dates, for example) → Used for **filtering**
- **CLUSTER** columns with **lower cardinality** → Used for **ordering**

### Applied to This Question
- **Filter column**: `tpep_dropoff_datetime` → **PARTITION**
- **Order by column**: `VendorID` → **CLUSTER**

**Answer: Partition by tpep_dropoff_datetime and Cluster on VendorID**

---

## Question 6. Partition Benefits

**Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive). Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?**

- 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
- **310.24 MB for non-partitioned table and 26.84 MB for the partitioned table** ✅
- 5.87 MB for non-partitioned table and 0 MB for the partitioned table
- 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table

### Queries

**Partitioned Table:**
```sql
SELECT DISTINCT(VendorID)
FROM `dtc-de-340821.zoomcamp.yellow_trip_data_materialized_partitioned`
WHERE tpep_dropoff_datetime >= '2024-03-01' 
  AND tpep_dropoff_datetime <= '2024-03-15';
```
**Estimate**: This query will process **26.84 MB** when run.

**Non-Partitioned Table:**
```sql
SELECT DISTINCT(VendorID)
FROM `dtc-de-340821.zoomcamp.yellow_trip_data_materialized` 
WHERE tpep_dropoff_datetime >= '2024-03-01' 
  AND tpep_dropoff_datetime <= '2024-03-15';
```
**Estimate**: This query will process **310.24 MB** when run.

### Performance Improvement
- **Reduction**: 91.3% fewer bytes scanned with partitioning
- **Why**: Partitioning allows BigQuery to skip irrelevant partitions (partition pruning)

**Answer: 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table**

---

## Question 7. External Table Storage

**Where is the data stored in the External Table you created?**

- Big Query
- Container Registry
- **GCP Bucket** ✅
- Big Table

### Explanation

External tables in BigQuery:
- Store data in **Google Cloud Storage (GCS) buckets**
- BigQuery only stores the schema and pointer to GCS files
- Data is **NOT** copied to BigQuery storage
- Queries read directly from GCS at runtime

**Answer: GCP Bucket**

---

## Question 8. Clustering Best Practices

**It is best practice in BigQuery to always cluster your data:**

- True
- **False** ✅

### Why It's FALSE

Clustering is **NOT** always best practice. It depends on:

1. **Table size** - Small tables don't benefit from clustering
2. **Query patterns** - If you don't filter/sort by specific columns, clustering adds no value
3. **Data characteristics** - High-cardinality unique columns make poor clustering keys
4. **Cost vs benefit** - Clustering has overhead that may not be worth it

### When to CLUSTER

✅ **DO Cluster when:**
- Table is **> 1 GB** in size
- You **frequently filter** by specific columns
- You **frequently ORDER BY** specific columns
- You use **GROUP BY** or **JOIN** on specific columns
- Query patterns are **predictable and repetitive**
- Column has **low to medium cardinality** (not unique IDs)

### When NOT to CLUSTER

❌ **DON'T Cluster when:**
- Table is **< 1 GB** (overhead > benefit)
- **Ad-hoc queries** with unpredictable patterns
- Column is **high-cardinality unique** (like `trip_id`, `user_id`)
- You **SELECT *** without filters (full table scans anyway)
- Table is **rarely queried**
- **Write-heavy** workloads (clustering adds overhead on inserts)

### Real-World Guidelines

| Table Size | Query Pattern | Cluster? | Reasoning |
|------------|---------------|----------|-----------|
| < 1 GB | Any | ❌ No | Table too small - overhead > benefit |
| 1-10 GB | Ad-hoc queries | ❌ No | Unpredictable patterns won't benefit |
| 1-10 GB | Repetitive filters on specific columns | ✅ Yes | Sweet spot for clustering benefits |
| > 10 GB | Ad-hoc queries | 🤔 Maybe | Consider if some common patterns exist |
| > 10 GB | Repetitive filters on specific columns | ✅ Definitely | Large data + predictable queries = maximum benefit |
| > 100 GB | Full table scans (SELECT *) | ❌ No | Clustering won't help full scans |
| > 100 GB | Filters on 2-3 key columns | ✅ Absolutely | Use up to 4 cluster columns for best results |

**Answer: False**

---

## Question 9. Understanding Table Scans

**No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?**

### Query
```sql
SELECT COUNT(*)
FROM `dtc-de-340821.zoomcamp.yellow_trip_data_materialized`;
```

### ✅ The Answer

**`COUNT(*)` doesn't need to read any data columns.**

BigQuery stores **table metadata** that includes the total row count. When you run `COUNT(*)` without WHERE conditions, BigQuery simply reads the metadata instead of scanning the entire table.

### Examples

```sql
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

### Why This Happens

1. **BigQuery stores metadata** with the total row count
2. **No columns specified** → No need to read column files
3. **No WHERE clause** → No filtering required
4. **Result**: Instant response from metadata (0 bytes processed)

### When COUNT(*) WILL Process Bytes

- ✅ **External tables** - Must scan GCS files
- ✅ **With WHERE clause** - Must scan to filter
- ✅ **COUNT(column)** - Must scan to count non-NULLs
- ✅ **With GROUP BY** - Must scan grouping columns

**Answer: 0 B - BigQuery reads the row count from table metadata**

---

## Summary Table

| Question | Answer | Key Concept |
|----------|--------|-------------|
| Q1 | 20,332,093 records | Counting external table records |
| Q2 | 0 MB / 155.12 MB | External table estimation limitation |
| Q3 | Columnar storage | BigQuery scans only requested columns |
| Q4 | 8,333 records | Filtering with WHERE clause |
| Q5 | Partition by date, Cluster by VendorID | Optimize for filter + order |
| Q6 | 310.24 MB / 26.84 MB | Partition pruning reduces scans by 91% |
| Q7 | GCP Bucket | External tables store data in GCS |
| Q8 | False | Clustering not always beneficial |
| Q9 | 0 B | COUNT(*) uses metadata |
