with trips_unioned as (
    select * from {{ ref('int_trips_unioned')}}
),

unioned_with_zones as (
    select
        t.*,
        z.borough as pickup_borough,
        z.zone as pickup_zone,
        z.service_zone as pickup_service_zone,
        ze.borough as dropoff_borough,
        ze.zone as dropoff_zone,
        ze.service_zone as dropoff_service_zone
    from trips_unioned t
    left join {{ ref('stg_taxi_zone_lookup') }} z
    on t.pickup_location_id = z.location_id
    left join {{ ref('stg_taxi_zone_lookup') }} ze 
    on t.dropoff_location_id = ze.location_id
)

select * from unioned_with_zones