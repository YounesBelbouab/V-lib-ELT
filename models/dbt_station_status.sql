{{ config(
    materialized='table'
) }}

WITH station_status_cte AS (
SELECT
    station_id,
    is_installed,
    is_renting,
    is_returning,
    num_bikes_available,
    num_docks_available,
FROM `velib-460309.velib_dataset.station_status`
--{% if is_incremental() %}
  --WHERE station_project_id NOT IN (SELECT station_project_id FROM {{ this }})
  WHERE station_id = 1
--{% endif %}
)

SELECT
*
FROM station_status_cte