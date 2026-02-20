with source as (
    select * from {{ source('raw_data', 'taxi_zone_lookup')}}
),

renamed as (
    select 
    cast(locationID as integer) as location_id,
    cast(Borough as string) as borough,
    cast(Zone as string) as zone,
    cast(service_zone as string) as service_zone

    from source
    where locationID is not null
)

select * from renamed