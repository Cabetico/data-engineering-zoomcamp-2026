## DATA WAREHOUSES

### OLAP vs OLTP


| Aspect | OLTP | OLAP |
|--------|------|------|
| **Purpose** | Mostly common in backend databases | Using for putting a lot of data in and discovering insights (analytical purposes) |
| **Data updates** | Short, fast updates initiated by user | Data periodically refreshed with scheduled, long-running batch jobs |
| **Database design** | Normalized databases for efficiency | Denormalized databases for analysis |
| **Space requirements** | Generally small if historical data is archived | Generally large due to aggregating large datasets |
| **Backups and recovery** | Regular backups required to ensure business continuity and meet legal and governance requirements | Lost data can be reloaded from OLTP database as needed in lieu of regular backups |
| **Productivity** | Increases productivity of end users | Increases productivity of business managers, data analysts, and executives |
| **Data view** | Lists day-to-day business transactions | Multi-dimensional view of enterprise data |
| **User examples** | Customer-facing personnel, clerks, online shoppers | Knowledge workers such as data analysts, business analysts, and executives |

##### OLTP (Online Transaction Processing) - Normalized
Purpose: Handle day-to-day operations and transactions

Characteristics:

* Normalized (3NF or higher) - data split into many related tables to eliminate redundancy
* Write-heavy - lots of INSERT, UPDATE, DELETE operations
* Small, fast queries - "Get user #123's order", "Update inventory for product X"
* Many concurrent users - hundreds/thousands of simultaneous transactions
* Data integrity is critical - ACID compliance, foreign keys, constraints
* Current data - focuses on the "now"

```SQL
    Users table: user_id, name, email
    Orders table: order_id, user_id, date
    OrderItems table: item_id, order_id, product_id, quantity
    Products table: product_id, name, price
```
Use Case: E-commerce site processing orders, banking transactions, inventory management

##### OLAP (Online Analytical Processing) - Denormalized
Purpose: Analyze historical data and generate insights

Characteristics:

* Denormalized - data combined into fewer, wider tables (often star/snowflake schema)
* Read-heavy - mostly SELECT queries for analysis
* Complex, long-running queries - "What were total sales by region last quarter?"
* Fewer concurrent users - analysts, BI tools
* Data redundancy is acceptable - optimized for query speed, not storage
* Historical data - stores data over time for trend analysis 

Example Schema (Star Schema):

* FactSales table: sale_id, date_id, product_id, customer_id, store_id, quantity, revenue
* DimDate table: date_id, date, month, quarter, year
* DimProduct table: product_id, name, category, subcategory
* DimCustomer table: customer_id, name, city, state, country
* DimStore table: store_id, store_name, region

| Aspect | OLTP (Normalized) | OLAP (Denormalized) |
|--------|------------------|---------------------|
| **Queries** | Simple, fast | Complex, slower |
| **Operations** | Read + Write | Mostly Read |
| **Data** | Current | Historical |
| **Users** | Many | Few |
| **Tables** | Many small tables | Few wide tables |
| **Joins** | Many joins needed | Fewer joins |
| **Goal** | Data integrity | Query performance |

### OLAP Data Flow Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐      │
│   │  Flat Files  │   │     OLTP     │   │    Other     │      │
│   │   (CSV,      │   │  Databases   │   │   Sources    │      │
│   │   JSON, etc) │   │              │   │  (APIs, etc) │      │
│   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘      │
│          │                  │                  │               │
└──────────┼──────────────────┼──────────────────┼───────────────┘
           │                  │                  │
           │                  │                  │
           └──────────────────┼──────────────────┘
                              │
                              ▼
           ┌──────────────────────────────────────┐
           │         STAGING AREA                 │
           │  (Temporary storage for ETL/ELT)     │
           │  - Data validation                   │
           │  - Data cleansing                    │
           │  - Data transformation               │
           └──────────────────┬───────────────────┘
                              │
                              ▼
           ┌──────────────────────────────────────┐
           │        DATA WAREHOUSE                │
           ├──────────────────────────────────────┤
           │  ┌────────────────────────────────┐  │
           │  │       Metadata               │  │
           │  │  (Schema, definitions, etc)   │  │
           │  └────────────────────────────────┘  │
           │  ┌────────────────────────────────┐  │
           │  │     Summary Data             │  │
           │  │  (Aggregated, pre-computed)   │  │
           │  └────────────────────────────────┘  │
           │  ┌────────────────────────────────┐  │
           │  │       Raw Data               │  │
           │  │  (Detailed historical data)   │  │
           │  └────────────────────────────────┘  │
           └──────────────────┬───────────────────┘
                              │
                              ▼
           ┌──────────────────────────────────────┐
           │          DATA MARTS                  │
           │  (Subject-specific subsets)          │
           ├──────────────────────────────────────┤
           │  ┌──────────┐  ┌──────────┐         │
           │  │  Sales   │  │ Finance  │  ...    │
           │  │   Mart   │  │   Mart   │         │
           │  └──────────┘  └──────────┘         │
           └──────────────────┬───────────────────┘
                              │
                              ▼
           ┌──────────────────────────────────────┐
           │       DOWNSTREAM USERS               │
           ├──────────────────────────────────────┤
           │  - Business Analysts                 │
           │  - Data Scientists                   │
           │  - Executives                        │
           │  - BI Tools & Dashboards             │
           │  - Reporting Systems                 │
           └──────────────────────────────────────┘
```

**Flow Summary:**
1. **Extract** data from multiple sources (Flat Files, OLTP, Other)
2. **Load** into Staging Area for cleaning and transformation
3. **Transform & Store** in Data Warehouse (organized into metadata, summary, and raw data)
4. **Distribute** to specialized Data Marts for specific business domains
5. **Consume** by downstream users for analysis and decision-making

### BigQuery

* Serverless data warehouse
  * There are no servers to manage or database software to install
 Software as well as infrastructure including
  * scalability and high-availability
* Built-in features like
  * machine learning
  * geospatial analysis
  * business intelligence
* BigQuery maximizes flesivility by separating the compute engine that analyzes your data from your storage


* Create external table from gs bucket with uris