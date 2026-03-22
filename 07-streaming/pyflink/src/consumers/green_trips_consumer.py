from datetime import datetime
from kafka import KafkaConsumer
import psycopg2
import json
import dataclasses
from dataclasses import dataclass

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
    
def green_ride_deserializer(data: bytes) -> GreenRide:
    return GreenRide(**json.loads(data.decode('utf-8')))

# --------------------------------------------------------------------------- #
#  Consumer + Postgres connection
# --------------------------------------------------------------------------- #

server = "localhost:9092"
topic_name = 'green-trips'

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[server],
    auto_offset_reset='earliest',
    group_id='green-trips-database',
    enable_auto_commit=True,
    value_deserializer=green_ride_deserializer,
)

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='postgres',
    user='postgres',
    password='postgres'
)
conn.autocommit = True
cur = conn.cursor()

# --------------------------------------------------------------------------- #
#  Create table if not exists
# --------------------------------------------------------------------------- #

cur.execute("""
    CREATE TABLE IF NOT EXISTS green_processed_events (
        PULocationID    INTEGER,
        DOLocationID    INTEGER,
        passenger_count DOUBLE PRECISION,
        trip_distance   DOUBLE PRECISION,
        tip_amount      DOUBLE PRECISION,
        total_amount    DOUBLE PRECISION,
        pickup_datetime  TIMESTAMP,
        dropoff_datetime TIMESTAMP
    )
""")
print("Table ready.")

# --------------------------------------------------------------------------- #
#  Consume
# --------------------------------------------------------------------------- #

print(f"Listening to '{topic_name}' and writing to PostgreSQL...")

count = 0
for message in consumer:
    ride = message.value

    pickup_dt  = datetime.fromisoformat(ride.lpep_pickup_datetime)
    dropoff_dt = datetime.fromisoformat(ride.lpep_dropoff_datetime)

    cur.execute(
        """INSERT INTO green_processed_events
           (PULocationID, DOLocationID, passenger_count,
            trip_distance, tip_amount, total_amount,
            pickup_datetime, dropoff_datetime)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (ride.PULocationID, ride.DOLocationID, ride.passenger_count,
         ride.trip_distance, ride.tip_amount, ride.total_amount,
         pickup_dt, dropoff_dt)
    )

    count += 1
    if count % 10000 == 0:
        print(f"Inserted {count} rows...")

consumer.close()
cur.close()
conn.close()