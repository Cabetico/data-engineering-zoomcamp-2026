"""dlt pipeline to ingest NYC taxi data from the Zoomcamp REST API."""

import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig


@dlt.source
def nyc_taxi_rest_api_source():
    """Define dlt resources from the NYC Taxi REST API."""
    config: RESTAPIConfig = {
        "client": {
            # NYC Taxi REST API base URL (no authentication required)
            "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
        },
        "resources": [
            {
                "name": "nyc_taxi_trips",
                "endpoint": {
                    # The Cloud Function URL already points at the data endpoint.
                    # We request 1,000 records per page and let the offset paginator
                    # advance `offset` until an empty page is returned.
                    "params": {
                        "limit": 1000,
                    },
                    "paginator": {
                        "type": "offset",
                        "limit": 1000,
                        # The API signals completion by returning an empty page,
                        # so we rely on that rather than a total count.
                        "total_path": None,
                        "stop_after_empty_page": True,
                    },
                },
            },
        ],
        # You can add `resource_defaults` here if you want to configure primary_key,
        # write_disposition, or common endpoint params for all resources.
    }

    yield from rest_api_resources(config)


taxi_pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    dataset_name="nyc_taxi_data",
    # Enable convenient local development behavior.
    dev_mode=True,
    # Show basic progress of resources extracted, normalized, and loaded.
    progress="log",
)


if __name__ == "__main__":
    load_info = taxi_pipeline.run(nyc_taxi_rest_api_source())
    print(load_info)  # noqa: T201

