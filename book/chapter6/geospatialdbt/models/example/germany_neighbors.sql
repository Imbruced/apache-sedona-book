{{ config(
    materialized='table',
    file_format='geoparquet'
)
}}
WITH germany AS (
    SELECT *
    FROM {{ source('air_quality', 'borders') }}
    WHERE country = 'DE'
)
SELECT
    n.country,
    n.geometry AS geom
FROM germany as g
JOIN {{ source('air_quality', 'borders') }} AS n ON ST_INTERSECTS(g.geometry, n.geometry)
