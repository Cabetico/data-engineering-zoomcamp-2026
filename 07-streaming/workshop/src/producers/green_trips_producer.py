import json
import dataclasses
from dataclasses import dataclass
from time import time
 
import pandas as pd
from kafka import KafkaProducer
 
 
# --------------------------------------------------------------------------- #
#  Model
# --------------------------------------------------------------------------- #
 
@dataclass
class GreenRide:
    lpep_pickup_datetime: str   # ISO-8601 string
    lpep_dropoff_datetime: str  # ISO-8601 string
    PULocationID: int
    DOLocationID: int
    passenger_count: float      # nullable in source, keep as float
    trip_distance: float
    tip_amount: float
    total_amount: float
 
 
def green_ride_from_row(row) -> GreenRide:
    return GreenRide(
        lpep_pickup_datetime=str(row['lpep_pickup_datetime']),
        lpep_dropoff_datetime=str(row['lpep_dropoff_datetime']),
        PULocationID=int(row['PULocationID']),
        DOLocationID=int(row['DOLocationID']),
        passenger_count=float(row['passenger_count']) if pd.notna(row['passenger_count']) else 0.0,
        trip_distance=float(row['trip_distance']),
        tip_amount=float(row['tip_amount']),
        total_amount=float(row['total_amount']),
    )
 
 
def green_ride_serializer(ride: GreenRide) -> bytes:
    return json.dumps(dataclasses.asdict(ride)).encode('utf-8')
 
 

 
 
# --------------------------------------------------------------------------- #
#  Load data
# --------------------------------------------------------------------------- #
 
URL = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet'
COLUMNS = [
    'lpep_pickup_datetime',
    'lpep_dropoff_datetime',
    'PULocationID',
    'DOLocationID',
    'passenger_count',
    'trip_distance',
    'tip_amount',
    'total_amount',
]
 
print("Loading parquet file...")
df = pd.read_parquet(URL, columns=COLUMNS)
print(f"Loaded {len(df):,} rows")
 
 
# --------------------------------------------------------------------------- #
#  Producer
# --------------------------------------------------------------------------- #
 
server = 'localhost:9092'
topic_name = 'green-trips'
 
producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=green_ride_serializer,
)
 
print(f"\nSending {len(df):,} rows to topic '{topic_name}'...")
 
t0 = time()
 
for _, row in df.iterrows():
    ride = green_ride_from_row(row)
    producer.send(topic_name, value=ride)
 
producer.flush()
 
t1 = time()
print(f'took {(t1 - t0):.2f} seconds')