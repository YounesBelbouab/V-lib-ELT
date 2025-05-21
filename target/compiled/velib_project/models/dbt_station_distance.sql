WITH stations AS (
    SELECT
        station_id,
        lat,
        lon
    FROM `velib-460309`.`velib_dataset`.`dbt_station_information`
),

pairs AS (
    SELECT
        a.station_id AS station_id_start,
        b.station_id AS station_id_closer,
        SQRT(
            POW(b.lat - a.lat, 2) +
            POW(b.lon - a.lon, 2)
        ) AS distance
    FROM stations a
    CROSS JOIN stations b
    WHERE a.station_id != b.station_id
),

ranked_distances AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY station_id_start ORDER BY distance ASC) AS rank
    FROM pairs
)

SELECT
    station_id_start,
    station_id_closer,
    ROUND(distance, 5) as distance,
FROM ranked_distances