"""@bruin
name: raw.taxi_trips
type: python
connection: duckdb-default
materialization:
  type: table
  strategy: append

columns:
  - name: vendor_id
    type: integer
    description: "Taxi vendor identifier"
  - name: pickup_datetime
    type: timestamp
    description: "Trip pickup datetime"
    checks:
      - name: not_null
  - name: dropoff_datetime
    type: timestamp
    description: "Trip dropoff datetime"
    checks:
      - name: not_null
  - name: passenger_count
    type: integer
    description: "Number of passengers"
    checks:
      - name: not_null
      - name: non_negative
  - name: trip_distance
    type: float
    description: "Trip distance in miles"
    checks:
      - name: non_negative
  - name: fare_amount
    type: float
    description: "Fare amount in USD"
  - name: total_amount
    type: float
    description: "Total amount charged"
@bruin""" 


import pandas as pd
import requests
import os
import io
import json

def materialize():
    """
    Fetches NY Yellow Taxi trip data from the NYC Open Data Parquet files
    hosted publicly, then returns a DataFrame for Bruin to load into DuckDB.
    """

    # NY Taxi data is available as Parquet files by month
    # This example fetches January 2024 yellow taxi trips
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"

    print(f"Fetching NY Taxi data from: {url}")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # Read parquet directly from the response bytes
    df = pd.read_parquet(io.BytesIO(response.content))

    # Select and rename only the columns we care about
    df = df[[
        "VendorID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "passenger_count",
        "trip_distance",
        "fare_amount",
        "total_amount",
    ]].rename(columns={
        "VendorID": "vendor_id",
        "tpep_pickup_datetime": "pickup_datetime",
        "tpep_dropoff_datetime": "dropoff_datetime",
    })

    # Basic cleanup: drop nulls in critical columns
    df = df.dropna(subset=["pickup_datetime", "dropoff_datetime"])
    df = df[df["passenger_count"] >= 0]
    df = df[df["trip_distance"] >= 0]

    print(f"Loaded {len(df):,} rows of taxi trip data.")
    return df

