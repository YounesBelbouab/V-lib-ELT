
  
    

    create or replace table `velib-460309`.`velib_dataset`.`dbt_bikes_available`
      
    
    

    OPTIONS()
    as (
      

WITH latest_status AS (
  SELECT
    MAX(last_reported) AS max_time
  FROM `velib-460309`.`velib_dataset`.`station_status`
),

bikes_now AS (
  SELECT
    SUM(num_bikes_available) AS total_bikes_available
  FROM `velib-460309`.`velib_dataset`.`station_status`
  WHERE last_reported = (SELECT max_time FROM latest_status)
)

SELECT
  total_bikes_available
FROM bikes_now
    );
  