# Module 6 Homework

In this homework we'll put what we learned about Spark in practice.

For this homework we will be using the Yellow 2025-11 data from the official website:

```bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet
```


## Question 1: Install Spark and PySpark

- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

What's the output?
A: '3.5.0'

> [!NOTE]
> To install PySpark follow this [guide](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-batch/setup/pyspark.md)


## Question 2: Yellow November 2025

Read the November 2025 Yellow into a Spark Dataframe.

Repartition the Dataframe to 4 partitions and save it to parquet.

What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

- 6MB
- 25MB ✅
- 75MB
- 100MB

A: 
```python
    # Read the parquet file into a Spark DataFrame
df = spark\
    .read\
    .parquet("/folder/yellow_tripdata_2025-11.parquet")

# Repartition to 4 partitions
df_repartitioned = df.repartition(4)

# Save to parquet
df_repartitioned\
    .write\
    .mode("overwrite")\
    .parquet("/folder/yellow_tripdata_2025-11_repartitioned/")

output_path = "/folder/yellow_tripdata_2025-11_repartitioned/"

parquet_files = [f for f in os.listdir(output_path) if f.endswith(".parquet")]

sizes_mb = [os.path.getsize(os.path.join(output_path, f)) / (1024 * 1024) for f in parquet_files]

avg_size_mb = sum(sizes_mb) / len(sizes_mb)

print(f"Number of parquet files: {len(parquet_files)}")
print(f"Individual sizes (MB): {[round(s, 2) for s in sizes_mb]}")
print(f"Average size: {round(avg_size_mb, 2)} MB")


Number of parquet files: 4
Individual sizes (MB): [26.37, 26.34, 26.31, 26.36]
Average size: 26.34 MB
``` 


## Question 3: Count records

How many taxi trips were there on the 15th of November?

Consider only trips that started on the 15th of November.

- 62,610
- 102,340
- 162,604 ✅
- 225,768

A: 
```python 
   
   import pyspark.sql.functions as f

   count = df.filter(f.to_date(f.col("tpep_pickup_datetime")) == "2025-11-15").count()
   print(f"Number of trips on November 15th: {count}") 

   Number of trips on November 15th: 162604
```


## Question 4: Longest trip

What is the length of the longest trip in the dataset in hours?

- 22.7
- 58.2
- 90.6 ✅
- 134.5

A:

```python 
df_with_duration = df.withColumn(
    "trip_duration_hours",
    (f.col("tpep_dropoff_datetime") - f.col("tpep_pickup_datetime")).cast("long") / 3600
)

longest_trip = df_with_duration.select(f.max("trip_duration_hours")).collect()[0][0]
longest_trip 

90.64666666666666
```


## Question 5: User Interface

Spark's User Interface which shows the application's dashboard runs on which local port?

- 80
- 443
- 4040 ✅
- 8080



## Question 6: Least frequent pickup location zone

Load the zone lookup data into a temp view in Spark:

```bash
wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

Using the zone lookup data and the Yellow November 2025 data, what is the name of the LEAST frequent pickup location Zone?

- Governor's Island/Ellis Island/Liberty Island ✅
- Arden Heights ✅
- Rikers Island
- Jamaica Bay

A: 
```python 

    df_zones = spark.read.option("header", "true").option("inferSchema", "true").csv("/folder/taxi_zone_lookup.csv")

    df_joined = df \
    .join(df_zones.withColumnRenamed("LocationID", "PULocationID")
                  .withColumnRenamed("Borough", "PU_Borough")
                  .withColumnRenamed("Zone", "PU_Zone")
                  .withColumnRenamed("service_zone", "PU_service_zone"),
          on="PULocationID", how="left") \
    .join(df_zones.withColumnRenamed("LocationID", "DOLocationID")
                  .withColumnRenamed("Borough", "DO_Borough")
                  .withColumnRenamed("Zone", "DO_Zone")
                  .withColumnRenamed("service_zone", "DO_service_zone"),
          on="DOLocationID", how="left")

    df_joined.groupBy("PU_Zone") \
    .agg(f.count("*").alias("trip_count")) \
    .orderBy("trip_count") \
    .show(5)

``` 

If multiple answers are correct, select any

## Submitting the solutions

- Form for submitting: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw6
- Deadline: See the website


## Learning in Public

We encourage everyone to share what they learned. This is called "learning in public".

Read more about the benefits [here](https://alexeyondata.substack.com/p/benefits-of-learning-in-public-and).

### Example post for LinkedIn

```
🚀 Week 6 of Data Engineering Zoomcamp by @DataTalksClub complete!

Just finished Module 6 - Batch Processing with Spark. Learned how to:

✅ Set up PySpark and create Spark sessions
✅ Read and process Parquet files at scale
✅ Repartition data for optimal performance
✅ Analyze millions of taxi trips with DataFrames
✅ Use Spark UI for monitoring jobs

Processing 4M+ taxi trips with Spark - distributed computing is powerful! 💪

Here's my homework solution: <LINK>

Following along with this amazing free course - who else is learning data engineering?

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

### Example post for Twitter/X

```
⚡ Module 6 of Data Engineering Zoomcamp done!

- Batch processing with Spark 🔥
- PySpark & DataFrames
- Parquet file optimization
- Spark UI on port 4040

My solution: <LINK>

Free course by @DataTalksClub: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```
