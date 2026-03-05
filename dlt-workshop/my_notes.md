## DLT

dlt → data loading tool

* an open-source Python library
* automates schema evolution, normalization, and data loading
* A lot of the actuals operations are done on your behalf, sounds like a describe what you need and not how to get it 



dlt 3-steps process
```python
import dlt
from dlt.sources.rest_api import rest_api_source
#source
source = rest_api_source(
    {
        "client": {
            "base_url": "https://jaffle-shop.dlthub.com/api/v1"
            },
            "resources": ["customers", "products", "stores"],
    },
)

#pipeline
pipeline = dlt.pipeline(
    pipeline_name="rest_api_example",
    destination="duckdb",
    dataset_name="rest_api_data"
)


pipeline.run(source)
```

### DEMO #1: The traditional way

```python
pipeline.run(source)
```

##### What does `pipeline.run()` do?
`pipeline.run()` simply combines the three steps we already executed manually:

* **Extract** – fetch data from the Open Library API
* **Normalize** – convert nested JSON into relational tables
* **Load** – write those tables into DuckDB

at the time of **extract** `dlt` does this things, considering this is part of `dlt` autonormalize
* Creates all the tables necesary under the hood considering the structure(nested JSON) of the json file 
* Infers data types 
* Automatically creates two IDs considering if your data do not have any id columns `_dlt_load_id`, `_dlt_id`
    * Creates childs tables
    * Creates own metadata tables


##### Conclusions

* In the previous notebook this script takes care of habdling the APIs logic itself. There is not need to hardcore
any logic for retries or pagination and other things of that nature, you only configure the source and all of that is done for you.

* You don't have to worry about normalizations, don't have to worry about making your laods compatible with the duckDB destination (JSON shredding)

* Don't need of pesky SQL queries just to connect to my duckdb database, I just can interact with my pipeline objects


```python
def openlibrary_source(query: str = "harry potter"):

    return rest_api_source({
        "client": {
            "base_url": "https://openlibrary.org",
            #token if the api neeeds
        },
        "resource_defaults": {
            "primary_key": "key",
            "write_disposition": "replace",
        },
        "resources": [
            {
                "name": "books",
                "endpoint": {
                    "path": "search.json",
                    "params": {
                        "q": query,
                        "limit": 100,
                    },
                    "data_selector": "docs",
                    "paginator": {
                        "type": "offset",
                        "limit": 100,
                        "offset_param": "offset",
                        "limit_param": "limit",
                        "total_path": "numFound",
                    },
                },
            },
        ],
    })
```

### THE CHALLENGE - Messy APIs [The dltHub Workspace Workflow]

* dltHub LLM scaffolds
    * Step 1: Load data - LLM scaffolds (templates for setting projects, writing projects to crate and run dlt pipelines) - Choose from over
        10,000 (and counting!) scaffolding templates of popular REST API data sources
    * Step 2: Ensure Quality (you can inspect pipeline, schema, data, and destination via)
        * dlt Dashboard
        * dlt MCP server
        * dlt CLI
    * Step 3: Create reports & transformations
        * Marimo? notebooks avoid stale outdated outpus
        * Explore, transform , and report from a single place
        * Based on Python code
            * version controlv
            * LLMs simply get it 
            * Ibis? database agnostics tools

### DEMO #2: The AI-Assosted Way

* `uv sync` for the repo
* `uv run dlt init dlthub:open_library duckdb` 


#### Start new project

### Interesting remarks about MCPs

Steps
* `uv init`
* `uv add "dlt[workspace]" `
*  `uv run dlt init dlthub:open_library duckdb` 
    * this command creates `.cursor` `.dlt`
    * `.corsor` has the folder `/rules` 
    * file `open_library-docs.yaml` is meant to be LLM readable
* `uv run dlt pipeline `

* MCP extends/enhances LLM agents capabilities beyond text in - text out
* LLM agents could use pre-defined MCP server functions