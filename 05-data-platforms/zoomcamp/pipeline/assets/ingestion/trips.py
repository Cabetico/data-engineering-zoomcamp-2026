"""@bruin
name: ingestion.trips
type: python
image: python:3.11
connection: duckdb-default

materialization:
  type: table
  strategy: append

columns:
  - name: pickup_datetime
    type: timestamp
    description: When the trip started (unified from tpep/lpep column)
  - name: dropoff_datetime
    type: timestamp
    description: When the trip ended (unified from tpep/lpep column)
  - name: taxi_type
    type: string
    description: Source taxi type (yellow, green)
  - name: extracted_at
    type: timestamp
    description: Timestamp when the row was extracted (for lineage/debugging)
@bruin"""

import os
import json
from datetime import datetime, timezone

import pandas as pd


def _parse_bruin_dates():
    start = os.environ.get("BRUIN_START_DATE")
    end = os.environ.get("BRUIN_END_DATE")
    if not start or not end:
        raise ValueError("BRUIN_START_DATE and BRUIN_END_DATE must be set (YYYY-MM-DD)")
    return start, end


def _parse_taxi_types():
    raw = os.environ.get("BRUIN_VARS", "{}")
    try:
        vars_ = json.loads(raw)
        return vars_.get("taxi_types", ["yellow"])
    except json.JSONDecodeError:
        return ["yellow"]


def _pickup_dropoff_columns(taxi_type: str):
    if taxi_type == "yellow":
        return "tpep_pickup_datetime", "tpep_dropoff_datetime"
    if taxi_type == "green":
        return "lpep_pickup_datetime", "lpep_dropoff_datetime"
    return "tpep_pickup_datetime", "tpep_dropoff_datetime"


def materialize():
    """
    Ingest NYC TLC trip data from the public parquet endpoint.
    Uses BRUIN_START_DATE, BRUIN_END_DATE and taxi_types variable to build
    the list of files to fetch. Keeps data in raw form; adds taxi_type and
    extracted_at for lineage. Normalizes pickup/dropoff datetime column names
    to pickup_datetime and dropoff_datetime for downstream staging.
    """
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"
    start_date, end_date = _parse_bruin_dates()
    taxi_types = _parse_taxi_types()

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    extracted_at = datetime.now(timezone.utc)
    frames = []

    for taxi_type in taxi_types:
        pickup_col, dropoff_col = _pickup_dropoff_columns(taxi_type)
        current = start.replace(day=1)
        while current <= end:
            year_month = current.strftime("%Y-%m")
            filename = f"{taxi_type}_tripdata_{year_month}.parquet"
            url = f"{base_url}/{filename}"
            try:
                df = pd.read_parquet(url)
                if df.empty:
                    current += pd.DateOffset(months=1)
                    continue
                # Normalize datetime column names for staging
                if pickup_col in df.columns:
                    df = df.rename(columns={pickup_col: "pickup_datetime"})
                if dropoff_col in df.columns and dropoff_col != pickup_col:
                    df = df.rename(columns={dropoff_col: "dropoff_datetime"})
                df["taxi_type"] = taxi_type
                df["extracted_at"] = extracted_at
                frames.append(df)
            except Exception:
                # Skip missing or failed months (e.g. future dates, network errors)
                pass
            current += pd.DateOffset(months=1)

    if not frames:
        return pd.DataFrame(
            columns=[
                "pickup_datetime",
                "dropoff_datetime",
                "taxi_type",
                "extracted_at",
            ]
        )
    return pd.concat(frames, ignore_index=True)
