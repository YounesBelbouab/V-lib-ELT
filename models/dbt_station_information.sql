{{ config(
    materialized='table'
) }}

WITH station_information_cte AS (
SELECT
    station_id,
    name,
    address,
    lat,
    lon,
    capacity,
FROM `velib-460309.velib_dataset.station_information`
--{% if is_incremental() %}
  --WHERE station_project_id NOT IN (SELECT station_project_id FROM {{ this }})
--{% endif %}
)

SELECT
*
FROM station_information_cte