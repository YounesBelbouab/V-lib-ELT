

WITH station_information_cte AS (
SELECT
    station_id,
    name,
    address,
    lat,
    lon,
    capacity,
FROM `velib-460309.velib_dataset.station_information`
--
)

SELECT
*
FROM station_information_cte