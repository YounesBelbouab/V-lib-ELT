
  
    

    create or replace table `velib-460309`.`velib_dataset`.`nb_vélo_disponible`
      
    
    

    OPTIONS()
    as (
      

WITH latest_status_per_station AS (
  SELECT
    station_id,
    MAX(last_reported) AS last_reported
  FROM `velib-460309`.`velib_dataset`.`station_status`
  GROUP BY station_id
),

bikes_latest_per_station AS (
  SELECT
    ss.station_id,
    ss.num_bikes_available
  FROM `velib-460309`.`velib_dataset`.`station_status` ss
  JOIN latest_status_per_station lsps
    ON ss.station_id = lsps.station_id
    AND ss.last_reported = lsps.last_reported
)

SELECT
  si.name AS name,
  blps.num_bikes_available
FROM bikes_latest_per_station blps
LEFT JOIN `velib-460309`.`velib_dataset`.`station_information` si
  ON blps.station_id = si.station_id
ORDER BY blps.num_bikes_available DESC
    );
  