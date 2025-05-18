WITH grid_with_measurement AS (
    SELECT distinct g.h3, g.country
    FROM {{ ref('grid') }} AS g
    JOIN {{ ref('neighbor_stations') }} AS s ON ST_Intersects(s.geom, g.geom)
), grid_all AS (
    SELECT
        country,
        count(*) AS total
    FROM {{ ref('grid') }} AS g
    GROUP BY country
),
grid_with_measurement_all AS (
    SELECT country, COUNT(*) AS total
    FROM grid_with_measurement
    GROUP BY country
),
grid_with_measurement_percentage AS (
    SELECT
        gwm.country,
        gwm.total / ga.total AS percentage
    FROM grid_with_measurement_all AS gwm
    JOIN grid_all AS ga ON gwm.country = ga.country
),
    pivot AS (
    SELECT
        *
    FROM grid_with_measurement_percentage
    PIVOT (
        SUM(percentage) AS percentage
        FOR country IN ('FR', 'BE', 'CH', 'LU', 'NL', 'DE', 'AT', 'CZ', 'PL')
    )
), filtering AS (
    SELECT (
        DE > 0.5 AND
        FR > 0.45 AND
        BE > 0.5 AND
        CH > 0.3 AND
        LU > 0.35 AND
        NL > 0.55 AND
        AT > 0.50 AND
        CZ > 0.55 AND
        PL > 0.60
    ) AS meet_criteria
    FROM pivot
)
SELECT *
FROM filtering
where NOT meet_criteria;


