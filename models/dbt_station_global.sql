WITH dbt_station_status_cte AS (
    SELECT *
    FROM {{ ref("dbt_station_status") }}
),

dbt_station_info_cte AS (
    SELECT *
    FROM {{ ref("dbt_station_information") }}
)

SELECT
    status.station_id,
    status.num_bikes_available,
    status.num_docks_available,
    status.is_renting,
    status.is_returning,
    info.name,
    info.capacity,
    info.lat,
    info.lon
FROM dbt_station_status_cte AS status
JOIN dbt_station_info_cte AS info
ON status.station_id = info.station_id
