# DBT(data build tool)
## What is dbt

dbt is a transformation workflow that allows anyone that knows SQL to deploy analytics code following software engineering best practices like modularity, portability, CI/CD, and documentation, the intention of dbt is to sit on top your data warehouse and provide the data consumers/ dowstream users something useful for BI, etc or machine learning workflow

## DBT layers
* Develop
* Test and document
* Deployment (Version control and CI/CD)

## How does dbt work

Each model is:
* A *.sql file
* Select statement, no DDL or DML
* A file that dbt will compile and ruin in our DWH
  
```
                      Modeling Layer
                    * Transform
                    *  Derived model
                         ^      │  
turn table into model    │      │ Persis back to data warehouse
                         │      │
                         |      v
                    Data warehouse
```

Once compiled the dbt code it's going to run the code upon your datawarehouse, transform the data and persist it back into the datawarehouse

## How to use dbt

### dbt Core
**Open-source project that allows the data transformation**
* builds and runs a dbt project (.sql and .yml files)
* Includes sQL compilation logic, macros and database adapters
* Includes a CLI interface to run dbt commands locally
* Opens source and free to use

### dbt Cloud
**Saas application to develop and manage dbt projects**

* Web=based IDE and cloud CLI to develop, run and test a dbt project
* Managed environments
* Jobs Orchestration
* Logging and Alerting
* Integrated documentation
* Admin and metada API
* Semantic Layer

### dbt cloud project

dbt provides an starter project with all the basic folders and files.
There are essentially two ways to use it: 

* With the CLI
* After having installed dbt locally and setup `profiles.yml`, run `dbt init` in the path we want to start the project to clone the starter project.

### With dbt cloud
After having et up the dbt clound credentials (repo and data warehouse) we can star a project from the web-based IDE

```
project/
├── analysis/
├── data/
├── macros/
├── models/
│   └── examples/
├── snapshots/
├── tests/
├── .gitignore
├── README.md
└── dbt_project.yml
```

## Modular data modeling

### Anatomy of a dbt model

Note: the `*.sql` scripts are models in dbt, dbt does the `DDL` `DML` for us 

* dbt model
```sql
{{ 
    config(materialized='table')
}}

SELECT *
FROM STAGING.SOURCE_TABLE
WHERE RECORD_STATE = 'ACTIVE'
```

* compiled code

```sql
create table my_schema.my_model as(
    Select *
    from staging.source_table
    where record_state  = 'ACTIVE'
)
```

#### Several materialization strategies
* Ephemeral: Ephemeral materializations are temporary and exist only for the duration of a single dbt run. Just Like a CTE in sql
* View: Views are virtual tables created by dbt that can be queried like regular tables, everytime you do a dbt run it's going to create or alter that view, the view stores the sql query rather than the data, when the source data is updated also updates the view
* Table: Tables ar ephysical representations of data that are created and store in the database
* Incremental: Incremental materializations are a powerful feature of dbt that allow for efficient updates to existing tables, reducing the need for full data refreshes

## the `FROM` clause of a dbt model

the basic diagram

```
    sources => clean sources => facts, dimension models
```

Sources
* The data loaded to our dwh that we use as sources for our models
* Configurations defined in the yml files in the models folder
* Used with the source macro that will resolve the name to the right schema, plus build the dependencies automatically
* Sources freshness can be defined and tested (how old the data is)

```yaml
sources: 
    - name: staging
      database: production
      schema: trip_data_all

      loaded_at_field: record_loaded_at
      tables:
       - name: green_tripdata
       - name: yellow_tripdata
        freshness: 
          error_after: {count: 6, period: hour}
```

```sql
    from {{ source('staging', 'yellow_tripdata_2021_01')}}
    where vendorid is not null
```

Seeds(similar to copy into)
* CSV files stored in our repository under the seed folder
* Benefits of version controlling
* Equivalent to a copy command
* Recommended for data that doesn't change frequently
* Runs with `dbt seed -s file_name`

```sql
select
    locationid,
    borough,
    zone,
    replace(service_zone, 'Boro', 'Green') as service_zone from 
    {{ ref('taxi_zone_lookup')}}
```
### About `Ref` function
* Macro to reference the underlying tables and views that were building the data warehouse
* Run the same code in any environment, it will resolve the correct schema for you
* Dependencies are built automatically


* dbt model
```sql
with green_data as (
    select *,
        'Green' as service_type
        from {{ ref('stg_green_tripdata')}}
)
```

* Compiled code

```sql
with green_data as (
    select *,
        'Green' as service_type
    from "production"."dbt_carlos_rodriguez"."stg_green_tripdata"
)
```

Note: the ref function help us to give some flexibility and avoid hardcoding sources in the compiled code injecting the referenced table of the current working env

Pause

## DBT Like a Pro with Bigquery 

* create project(let's use uv for this)

step 1 install libraries
* install libraries dbt-core, dbt-bigquery

step 2
   * `dbt init`
   *  This will ask you for a name for the project

step 3(config):
  * which database would you like to use?
      * bigquery
  * Desired ahthetication method option (enter a number):
    * project_id: 
    * dataset: zoomcamp?
  
step 4: 
    after config run `dbt debug` to validate the connection


run dbt
`dbt run --model <name of model>`

