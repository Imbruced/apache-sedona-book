{{ config(
    materialized='table',
    file_format='geoparquet'
)
}}
WITH combined AS (
    SELECT
        o.*,
        hour(o.start_time) AS measurement_hour,
        date(o.start_time) AS measurement_date,
        s.geom,
        s.country,
        s.pollutant
    FROM {{ ref('observations') }} AS o
    JOIN {{ ref('stations') }} AS s ON o.sampling_id = s.sampling_id
    WHERE date(o.start_time) >= '2023-12-01'
),
    grid AS (
    SELECT
        g.h3,
        g.country,
        g.geom
    FROM {{ ref('grid') }} AS g
    WHERE g.level = 5
),
    grid_values AS (
    SELECT
        c.*,
        g.h3,
        g.geom as h3_geom
    FROM combined AS c
    JOIN grid AS g ON ST_Intersects(c.geom, g.geom)
)
SELECT
    g.country,
    g.h3,
    FIRST(g.h3_geom) AS geom,
    measurement_date,
    measurement_hour,
    AVG(measurement) AS avg_measurement,
    pollutant
FROM grid_values AS g
GROUP BY g.country, g.h3, pollutant, measurement_date, measurement_hour;

