{{ config(
    materialized='table',
    file_format='geoparquet')
}}
WITH UNIQUE_GRID AS (
    SELECT distinct h3, country, 4 as level
    FROM {{ ref('germany_neighbors') }}
    LATERAL VIEW EXPLODE (ST_H3CellIDs(geom, 4, true)) AS h3
    UNION ALL
    SELECT distinct h3, country, 5 as level
    FROM {{ ref('germany_neighbors') }}
    LATERAL VIEW EXPLODE (ST_H3CellIDs(geom, 5, true)) AS h3
),
INDEXES AS (
    SELECT
        h3,
        geom,
        country,
        level
    FROM UNIQUE_GRID
    LATERAL VIEW EXPLODE (ST_H3ToGeom(ARRAY(h3))) AS geom
)
SELECT
    i.h3,
    i.geom,
    i.country,
    i.level
FROM INDEXES AS i
JOIN {{ ref('germany_neighbors') }} AS n ON ST_Intersects(i.geom, n.geom);
