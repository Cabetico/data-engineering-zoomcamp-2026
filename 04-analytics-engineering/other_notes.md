# ANALYTICS ENGINEER BASICS

## DATA DOMAIN DEVELOPMENTS
* Massively parallel processing (MPP) databases
    * Massively Parallel Processing (MPP) Databases
    BigQuery, Snowflake, Redshift, Azure Synapse, Databricks, Hive, Presto, Trino
* Data-pipelines-as-a-service
    * Apache Airflow, Astronomer, Prefect, Dagster, Fivetran, Airbyte, Mage, dlt, AWS Glue, Azure Data Factory, Google Cloud Dataflow
* SQL-first
    * dbt (data build tool), SQLMesh, dbt Cloud, Dataform, Google Looker, Mode Analytics
* Version control systems
    * Git, GitHub, GitLab, Bitbucket, Azure DevOps, DVC (Data Version Control), LakeFS (data lake versioning)
* Self service analytics
    * Tableau, Looker, Power BI, Metabase, Apache Superset, Redash, Google Data Studio / Looker Studio, Preset, Sigma
* Data Governance
   * Apache Atlas, Collibra, Alation, DataHub, OpenMetadata, Google Dataplex, AWS Glue Data Catalog, Informatica, Monte Carlo (data observability)
  
## ROLES IN A DATA TEAM
Motivation: Analytist and Data Scientist are nowdays writing more and more code but the are not training in software development good practices

Data Engineer: Prepares and maintain the infrastructure the data team needs.

Data analyst: Uses data to answer questions and solve problems

Analytics Engineer: Introduces the good software engineering practices to the efforts of data analysts and data scientists

## TOOLING FOR THE ANALYTIS ENGINEER

Data Loading
=>
Data Storing (Cloud data warehouses like Snowflake, BigQuery, Redshift)
=>
Data modelling (Tools like dbt or Dataform)
=>
Data presentation
BI tools like google data studio, Looker, Mode or Tableau

## DATA MODELING CONCEPTS
### ETL vs ELT refresh

* ETL
  - Slightly more stable and compliant data analysis
  - Higher storage and compute costs
  - Load, transform data(this phase is time consuming) and load it to Data Warehouse
* ELT
  - Faster and more flexible data analysis
  - Lower cost and lower maintenance 
  - Only Load and transform it inside the Data Warehouse

### Kimball's Dimensional Modeling
Objective
* Deliver data understandable to the business users
* Deliver fast query performance

Approach
Prioritise user understandability and query performance over non redundant data (3NF)


#### 3NF Database Example - Business Case: Music Streaming Service - Tables

**artists**
| artist_id (PK) | artist_name   | country |
|----------------|---------------|---------|
| 1              | The Beatles   | UK      |
| 2              | Taylor Swift  | US      |

**albums**
| album_id (PK) | artist_id (FK) | album_title        | release_year |
|---------------|----------------|--------------------|--------------|
| 1             | 1              | Abbey Road         | 1969         |
| 2             | 2              | Fearless           | 2008         |

**songs**
| song_id (PK) | album_id (FK) | song_title         | duration_sec |
|--------------|---------------|--------------------|--------------|
| 1            | 1             | Come Together      | 259          |
| 2            | 1             | Something          | 182          |
| 3            | 2             | Love Story         | 235          |

#### Why It's 3NF Compliant

- **1NF** → Every column has atomic values, no repeating groups
- **2NF** → Every non-key column depends on the **full** primary key
- **3NF** → No transitive dependencies (e.g. `country` lives in `artists`, not in `albums` or `songs`)

#### Key Relationships
- One `artist` → Many `albums`
- One `album` → Many `songs`


### LEVELS OF NF

#### 1. Atomic Values & No Repeating Groups (1NF)

#### **Atomic Values**

**Atomic = one single value per cell, not a list or multiple values.**

#### ❌ NOT Atomic (violates 1NF)

| song_id | song_title     | genres            |
|---------|----------------|-------------------|
| 1       | Come Together  | rock, blues, pop  |
| 2       | Love Story     | pop, country      |

The `genres` column has **multiple values in one cell** → not atomic.

#### ✅ Atomic

| song_id | genre_id | song_title    |
|---------|----------|---------------|
| 1       | 1        | Come Together |
| 1       | 2        | Come Together |
| 2       | 3        | Love Story    |

Each cell has **exactly one value**.

---

#### No Repeating Groups

**No repeating groups = don't create multiple columns to store the same type of data.**

##### ❌ Repeating Groups (violates 1NF)

| album_id | album_title | song_1        | song_2    | song_3  |
|----------|-------------|---------------|-----------|---------|
| 1        | Abbey Road  | Come Together | Something | Octopus |

The columns `song_1`, `song_2`, `song_3` are the **same type of data repeated** → violates 1NF.

##### ✅ No Repeating Groups

| song_id | album_id | song_title    |
|---------|----------|---------------|
| 1       | 1        | Come Together |
| 2       | 1        | Something     |
| 3       | 1        | Octopus       |

Each song gets **its own row** instead of its own column.

---

#### Simple Mental Check

> **Atomic**: *"Can I split this cell value further?"* → If yes, it's not atomic.
>
> **Repeating groups**: *"Am I creating columns like `thing_1`, `thing_2`, `thing_3`?"* → If yes, make it a new table instead.

---

#### 2. 2NF — Full Primary Key Dependency

2NF only matters when you have a **composite primary key** (a PK made of 2+ columns).

**Every non-key column must depend on the FULL primary key, not just part of it.**

#### Example: Song Plays Table

Imagine tracking which users play which songs, with a composite PK of `(user_id, song_id)`.

#### ❌ Violates 2NF

| user_id (PK) | song_id (PK) | play_count | song_title    | user_name |
|--------------|--------------|------------|---------------|-----------|
| 1            | 101          | 5          | Come Together | Alice     |
| 1            | 102          | 3          | Love Story    | Alice     |
| 2            | 101          | 8          | Come Together | Bob       |

**The problem:**
- `play_count` → depends on **both** `user_id + song_id` ✅
- `song_title` → depends **only** on `song_id` ❌ (partial dependency)
- `user_name` → depends **only** on `user_id` ❌ (partial dependency)

#### ✅ 2NF Compliant — Split into 3 tables

**users**

| user_id (PK) | user_name |
|--------------|-----------|
| 1            | Alice     |
| 2            | Bob       |

**songs**

| song_id (PK) | song_title    |
|--------------|---------------|
| 101          | Come Together |
| 102          | Love Story    |

**plays**

| user_id (PK, FK) | song_id (PK, FK) | play_count |
|------------------|------------------|------------|
| 1                | 101              | 5          |
| 1                | 102              | 3          |
| 2                | 101              | 8          |

Now `play_count` is the **only non-key column** in `plays`, and it correctly depends on the **full composite key** `(user_id + song_id)`.

---

#### Simple Mental Check

> *"If I only knew half of the primary key, could I still determine this column's value?"*
>
> **Yes** → Partial dependency → **violates 2NF** → move it to its own table.
> **No** → Depends on full key → **2NF compliant** ✅

> **Important:** If your table has a **single-column primary key**, it is **automatically 2NF compliant** because there's no "partial" key to depend on.

---

#### 3. 3NF — No Transitive Dependencies

**A non-key column should NOT depend on another non-key column.**

In other words: **every column must depend on the key, the whole key, and nothing but the key.**

#### Example

#### ❌ Violates 3NF (Transitive Dependency)

| artist_id (PK) | artist_name  | country_code | country_name   |
|----------------|--------------|--------------|----------------|
| 1              | The Beatles  | UK           | United Kingdom |
| 2              | Taylor Swift | US           | United States  |
| 3              | Bad Bunny    | PR           | Puerto Rico    |

**The problem:**
- `country_code` → depends on `artist_id` ✅
- `country_name` → depends on `country_code` ❌ (not on `artist_id`!)

```
artist_id → country_code → country_name
```

`country_name` depends on `artist_id` **only indirectly**, through `country_code`. That indirect chain is called a **transitive dependency**.

#### ✅ 3NF Compliant — Split into 2 tables

**artists**

| artist_id (PK) | artist_name  | country_code (FK) |
|----------------|--------------|-------------------|
| 1              | The Beatles  | UK                |
| 2              | Taylor Swift | US                |
| 3              | Bad Bunny    | PR                |

**countries**

| country_code (PK) | country_name   |
|-------------------|----------------|
| UK                | United Kingdom |
| US                | United States  |
| PR                | Puerto Rico    |

---

#### The Chain Analogy

```
❌ Transitive (3NF violation):
PK → non-key column A → non-key column B

✅ 3NF Compliant:
PK → non-key column A
PK → non-key column B   (both point directly to the PK)
```

#### Simple Mental Check

> *"Does this column depend on another **non-key** column instead of directly on the primary key?"*
>
> **Yes** → Transitive dependency → **violates 3NF** → move it to its own table.
> **No** → Depends directly on PK → **3NF compliant** ✅

---

#### 4. Inmon Approach — "Top-Down"

Bill Inmon is considered the **"Father of Data Warehousing"**. His approach builds a **centralized, normalized warehouse first**, then serves data to downstream systems.

#### Core Idea

```
Source Systems → ETL → Enterprise Data Warehouse (3NF) → Data Marts
```

- The **EDW (Enterprise Data Warehouse)** is the single source of truth
- Data is stored in **3NF** (normalized)
- **Data Marts** are built on top for specific business areas (sales, finance, HR)

#### Key Characteristics

| Aspect           | Inmon                          |
|------------------|--------------------------------|
| **Direction**    | Top-Down                       |
| **Storage model**| 3NF normalized                 |
| **Starting point**| Enterprise-wide warehouse first|
| **Data Marts**   | Derived from EDW               |
| **Redundancy**   | Minimal (normalized)           |
| **Flexibility**  | High (easy to add new marts)   |
| **Complexity**   | High upfront effort            |
| **Query speed**  | Slower (many joins needed)     |

#### Visual

```
                    ┌─────────────────────┐
   Source           │  Enterprise Data    │
   Systems  ──ETL──▶│  Warehouse (3NF)   │
                    │  Single source      │
                    │  of truth           │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │  Sales   │    │ Finance  │    │    HR    │
        │   Mart   │    │   Mart   │    │   Mart   │
        └──────────┘    └──────────┘    └──────────┘
              └────────────────┼────────────────┘
                               ▼
                        Business Users
```

#### Pros and Cons

**✅ Pros:**
- Single source of truth for the entire organization
- Minimal data redundancy (3NF)
- Easy to add new data marts without restructuring
- Great data consistency and integrity
- Audit-friendly (good for regulated industries)

**❌ Cons:**
- Very complex and expensive to build upfront
- Takes longer to deliver value to business users
- Requires lots of ETL development
- Many joins needed → slower queries
- Needs strong data modeling expertise

---

## 5. EDW — Enterprise Data Warehouse

The **central repository** that stores ALL of an organization's data in one place.

### Simple Analogy

```
❌ Without EDW:                    ✅ With EDW:
Each department has                One central library
its own bookshelf                  everyone shares
(sales, finance, HR)
→ Same book in 3 places            → One copy, always up to date
→ Different versions               → Single source of truth
→ Hard to cross-reference          → Easy to combine data
```

### EDW vs Regular Database

|                  | Operational DB (OLTP)    | EDW (OLAP)                        |
|------------------|--------------------------|-----------------------------------|
| **Purpose**      | Run the business         | Analyze the business              |
| **Queries**      | Many small transactions  | Few large analytical queries      |
| **Data**         | Current data only        | Historical data                   |
| **Example**      | "Process this order"     | "Show all orders from 2020-2024"  |
| **Tools**        | PostgreSQL, MySQL        | BigQuery, Snowflake, Redshift     |

> **One Line Definition:** The single place where ALL company data lives, cleaned, integrated, and ready for analysis.

---

## 6. Data Vault

A data modeling methodology designed for **enterprise data warehouses** that focuses on **flexibility, auditability, and handling change** over time. Created by **Dan Linstedt** in the 1990s.

### Core Building Blocks

Data Vault has only **3 types of tables**:

#### 🔑 Hubs — "The Business Keys"
Stores the **unique business entities** (what things ARE).

| hub_customer_id (PK) | customer_id (BK) | load_date  | record_source |
|----------------------|------------------|------------|---------------|
| abc123               | CUST-001         | 2024-01-01 | CRM           |
| def456               | CUST-002         | 2024-01-01 | CRM           |

#### 🔗 Links — "The Relationships"
Stores **relationships between hubs** (how things CONNECT).

| link_order_id (PK) | hub_customer_id (FK) | hub_product_id (FK) | load_date  |
|--------------------|----------------------|---------------------|------------|
| xyz789             | abc123               | prod001             | 2024-01-01 |

#### 📋 Satellites — "The Context/Attributes"
Stores **descriptive attributes and history** (what things LOOK LIKE over time).

| hub_customer_id (FK) | load_date  | customer_name | country | record_source |
|----------------------|------------|---------------|---------|---------------|
| abc123               | 2024-01-01 | Alice Smith   | US      | CRM           |
| abc123               | 2024-06-01 | Alice Johnson | US      | CRM           |

> Notice Alice changed her last name — **Data Vault keeps ALL history** automatically!

### Visual Structure

```
          ┌─────────────────┐
          │   HUB Customer  │
          │   (who)         │
          └────────┬────────┘
                   │
         ┌─────────┴──────────┐
         ▼                    ▼
┌─────────────────┐  ┌─────────────────┐
│ SAT Customer    │  │  LINK           │
│ Demographics    │  │  Order          │
│ (attributes)    │  │  (relationship) │
└─────────────────┘  └────────┬────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
           ┌──────────────┐     ┌──────────────────┐
           │  HUB Product │     │  SAT Order       │
           │  (what)      │     │  Details         │
           └──────────────┘     │  (attributes)    │
                                └──────────────────┘
```

### Key Characteristics

| Aspect               | Data Vault                              |
|----------------------|-----------------------------------------|
| **Direction**        | Middle-out                              |
| **Storage model**    | Hubs + Links + Satellites               |
| **History tracking** | Built-in (all changes kept)             |
| **Auditability**     | Very high (`load_date`, `record_source`)|
| **Flexibility**      | Very high (easy to add new sources)     |
| **Complexity**       | High                                    |
| **Query speed**      | Slow (many joins needed)                |

### Mandatory Metadata Columns

Every Data Vault table **always** has these columns:

```sql
load_date       -- When was this record loaded?
record_source   -- Where did this record come from?
```

### Where It Fits in the Stack

```
Source Systems
      ↓
   Staging
      ↓
 Data Vault          ← Raw, auditable, historical
 (EDW Layer)
      ↓
 Presentation        ← Star Schema / Kimball
 Layer (Data Marts)
      ↓
 Business Users
```

> **Data Vault is NOT for end users** — you always build a Kimball-style presentation layer on top for reporting.

### Pros and Cons

**✅ Pros:**
- Handles change very well (new sources, new columns)
- Full historical tracking built-in
- Highly auditable (great for regulated industries)
- Parallel loading (hubs, links, satellites load independently)
- Easy to integrate multiple source systems

**❌ Cons:**
- Very complex to build and maintain
- Lots of tables (can have hundreds in large orgs)
- Slow query performance (many joins)
- Not user-friendly (needs a presentation layer on top)
- Steep learning curve

---

## 7. The Big Three Compared

| Aspect               | Inmon          | Kimball        | Data Vault          |
|----------------------|----------------|----------------|---------------------|
| **Model**            | 3NF            | Star Schema    | Hubs/Links/Sats     |
| **Direction**        | Top-Down       | Bottom-Up      | Middle-Out          |
| **History**          | Limited        | Limited        | Full (built-in)     |
| **Flexibility**      | Medium         | Low            | Very High           |
| **Complexity**       | High           | Low            | Very High           |
| **Query Speed**      | Slow           | Fast           | Very Slow           |
| **Best for**         | Large enterprises | Agile/BI teams | Regulated industries |
| **End user friendly**| No             | Yes            | No (needs layer)    |

---

## Summary: Normal Forms Quick Reference

| Normal Form | Rule | Key Question |
|-------------|------|--------------|
| **1NF** | Atomic values, no repeating groups | *"Does any cell have multiple values or repeated columns?"* |
| **2NF** | No partial dependencies (composite PKs) | *"Does any column depend on only PART of the PK?"* |
| **3NF** | No transitive dependencies | *"Does any column depend on a NON-KEY column?"* |

Other Approaches
Bill inmon
Data vault

Facts tables 
* Measurements, metrics or facts
* Corresponds to a business process
* think about them as "verbs" (Sells, Orders)

Dimensions tables
* Corresponds to a business entity
* Provides context to a business process
* think about them as "nouns" (costumers, products)


### Architecture of Dimensional Modeling
Stage Area
*  Contains the raw data
*  Not meant to be exposed to everyone
  
Processing Are
* From rawa data to data models
* Focuses in efficiency
* Ensuring standards

Presentation Area
* final presentation of the data
* Exposure to business stakeholder
