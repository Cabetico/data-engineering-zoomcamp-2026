# Quiz Questions

Complete the quiz shown below. It's a set of 6 multiple-choice questions to test your understanding of workflow orchestration, Kestra, and ETL pipelines.

---

## Question 1

**Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e. the output file `yellow_tripdata_2020-12.csv` of the extract task)?**

- 128.3 MiB
- 134.5 MiB
- 364.7 MiB
- 692.6 MiB

![CSV File Size](images/gcp_csv.png)

**Answer:** 134.5 MiB

---

## Question 2

**What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?**

- `{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv`
- `green_tripdata_2020-04.csv`
- `green_tripdata_04_2020.csv`
- `green_tripdata_2020.csv`

### Flow Configuration
```yaml
id: render_value
namespace: zoomcamp

inputs:
  - id: taxi
    type: SELECT
    displayName: Select
    values: [yellow, green]
    defaults: green

  - id: year
    type: SELECT
    displayName: Select
    values: ["2019", "2020"]
    defaults: "2019"

  - id: month
    type: SELECT
    displayName: Select month
    values: ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    defaults: "01"

variables:
  file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"
  staging_table: "public.{{inputs.taxi}}_tripdata_staging"
  table: "public.{{inputs.taxi}}_tripdata"
  data: "{{outputs.extract.outputFiles[inputs.taxi ~ '_tripdata_' ~ inputs.year ~ '-' ~ inputs.month ~ '.csv']}}"

tasks:
  - id: debug_file
    type: io.kestra.plugin.core.log.Log
    message: "DEBUG - File variable: {{render(vars.file)}}"
    level: DEBUG
```

![Log Output](images/log_value.png)

**Answer:** `green_tripdata_2020-04.csv`

---

## Question 3

**How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?**

- 13,537,299
- 24,648,499
- 18,324,219
- 29,430,127

### Query Used
```sql
WITH file_year_table AS 
( 
  SELECT 
    tpep_pickup_datetime,
    CAST(EXTRACT(YEAR FROM tpep_pickup_datetime) AS STRING) AS file_year
  FROM `dtc-de-340821.zoomcamp.yellow_tripdata`
) 
SELECT
  file_year, 
  COUNT(*)
FROM file_year_table
WHERE file_year = '2020'  
GROUP BY file_year;
```

**Answer:** 24,648,663

---

## Question 4

**How many rows are there for the Green Taxi data for all CSV files in the year 2020?**

- 5,327,301
- 936,199
- 1,734,051
- 1,342,034

### Query Used
```sql
WITH file_year_table AS 
( 
  SELECT 
    filename,
    SUBSTRING(filename FROM '\d{4}') AS file_year
  FROM green_tripdata
) 
SELECT
  file_year, 
  COUNT(*)
FROM file_year_table
WHERE file_year = '2020'  
GROUP BY file_year;
```

**Answer:** 1,734,051

---

## Question 5

**How many rows are there for the Yellow Taxi data for the March 2021 CSV file?**

- 1,428,092
- 706,911
- 1,925,152
- 2,561,031

### Query Used
```sql
WITH file_date_table AS 
( 
  SELECT 
    tpep_pickup_datetime,
    CAST(EXTRACT(YEAR FROM tpep_pickup_datetime) AS STRING) AS file_year,
    CAST(EXTRACT(MONTH FROM tpep_pickup_datetime) AS STRING) AS file_month
  FROM `dtc-de-340821.zoomcamp.yellow_tripdata`
) 
SELECT
  file_year,
  file_month,
  COUNT(*)
FROM file_date_table
WHERE file_month = '3' AND file_year = '2021'  
GROUP BY file_year, file_month
ORDER BY file_month;
```

**Answer:** 1,925,130

---

## Question 6

**How would you configure the timezone to New York in a Schedule trigger?**

- Add a `timezone` property set to `EST` in the Schedule trigger configuration
- Add a `timezone` property set to `America/New_York` in the Schedule trigger configuration
- Add a `timezone` property set to `UTC-5` in the Schedule trigger configuration
- Add a `location` property set to `New_York` in the Schedule trigger configuration

**Answer:** Add a `timezone` property set to `America/New_York` in the Schedule trigger configuration