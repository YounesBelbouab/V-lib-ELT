WITH base AS (
  SELECT
    si.station_id AS station_id,
    si.name AS name,
    si.address,
    si.lat,
    si.lon,
    si.capacity,
    ss.is_installed,
    ss.is_renting,
    ss.is_returning,
    ss.num_bikes_available,
    ss.num_docks_available
  FROM {{ source('velib_dataset', 'station_information') }} si
  LEFT JOIN {{ source('velib_dataset', 'station_status') }} ss
    ON si.station_id = ss.station_id
),

distances AS (
  SELECT
    a.station_id AS station_id,
    a.name AS name,
    a.lat AS lat_a,
    a.lon AS lon_a,
    b.station_id AS closest_station_id,
    b.name AS closest_station_name,
    b.lat AS lat_b,
    b.lon AS lon_b,
    6371 * ACOS(
      COS(a.lat * 3.141592653589793 / 180) * COS(b.lat * 3.141592653589793 / 180) *
      COS((b.lon - a.lon) * 3.141592653589793 / 180) +
      SIN(a.lat * 3.141592653589793 / 180) * SIN(b.lat * 3.141592653589793 / 180)
    ) AS distance_km
  FROM {{ source('velib_dataset', 'station_information') }} a
  JOIN {{ source('velib_dataset', 'station_information') }} b
    ON a.station_id != b.station_id
),

min_distances AS (
  SELECT
    station_id,
    name,
    ARRAY_AGG(STRUCT(closest_station_id, closest_station_name, distance_km)
              ORDER BY distance_km ASC)[OFFSET(0)] AS nearest
  FROM distances
  GROUP BY ALL
)

SELECT DISTINCT
  b.*,
  m.nearest.closest_station_id,
  m.nearest.closest_station_name,
  ROUND(m.nearest.distance_km, 3) AS distance_km_to_closest
FROM base b
JOIN min_distances m
  ON b.station_id = m.station_id
