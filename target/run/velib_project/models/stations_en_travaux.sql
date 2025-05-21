

  create or replace view `velib-460309`.`velib_dataset`.`stations_en_travaux`
  OPTIONS()
  as 

WITH station_status AS (
    SELECT
        station_id,
        is_installed,
        is_renting,
        is_returning,
        last_reported
    FROM `velib-460309.velib_dataset.station_status`
),

station_information AS (
    SELECT
        station_id,
        name,
        address,
        lat,
        lon
    FROM `velib-460309.velib_dataset.station_information`
)

SELECT
    info.station_id,
    info.name,
    info.address,
    info.lat,
    info.lon,
    status.is_installed,
    status.is_renting,
    status.is_returning,
    status.last_reported
FROM station_status AS status
JOIN station_information AS info
    ON status.station_id = info.station_id
WHERE status.is_installed = 0
   OR status.is_renting = 0
   OR status.is_returning = 0;

