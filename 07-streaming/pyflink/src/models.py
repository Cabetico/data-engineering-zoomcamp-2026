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