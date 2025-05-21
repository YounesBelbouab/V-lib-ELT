

  create or replace view `velib-460309`.`velib_dataset`.`dbt_station_global`
  OPTIONS()
  as WITH station_information_cte AS (
    SELECT
        station_id,
        name,
        lat,
        lon,
        capacity
    FROM `velib-460309`.`velib_dataset`.`dbt_station_information`
),

station_status_cte AS (
    SELECT
        station_id,
        is_installed,
        is_renting,
        is_returning,
        num_bikes_available,
        num_docks_available,
        last_reported,
    FROM `velib-460309`.`velib_dataset`.`dbt_station_status`
),

station_global AS (
    SELECT DISTINCT
        s.station_id,
        s.name,
        s.lat,
        s.lon,
        s.capacity,
        st.is_installed,
        st.is_renting,
        st.is_returning,
        st.num_bikes_available,
        st.num_docks_available,
        st.last_reported,
    FROM station_information_cte s
    JOIN station_status_cte st
        ON s.station_id = st.station_id
)

SELECT DISTINCT *
FROM station_global;

