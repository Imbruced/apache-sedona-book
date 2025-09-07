{{
    config(
        materialized='table',
        file_format='geoparquet'
    )
}}
WITH neighor_stations AS (
    SELECT *
    FROM {{ ref('stations_raw') }}
    WHERE country in (
        'Poland',
        'Czechia',
        'Austria',
        'Switzerland',
        'France',
        'Luxembourg',
        'Belgium',
        'Netherlands',
        'Denmark',
        'Germany'
    )
)
SELECT
    DISTINCT lower(concat(iso_code, "/", `sampling_id`)) AS sampling_id,
    country,
    ST_POINT(lon, lat) AS geom,
    air_pollutant AS pollutant
FROM neighor_stations as s
WHERE ST_POINT(lon, lat) IS NOT NULL