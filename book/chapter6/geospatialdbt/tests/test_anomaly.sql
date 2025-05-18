WITH close_stations AS (
    SELECT o1.sampling_id AS sampling_id1, o2.sampling_id AS sampling_id2
    FROM {{ref('neighbor_stations')}} as o1
    JOIN {{ref('neighbor_stations')}} as o2 ON ST_Distance(o1.geom, o2.geom) < 0.1
    WHERE o1.sampling_id != o2.sampling_id
)
SELECT cs.*
FROM close_stations as cs
-- JOIN {{ref('observations')}} as o ON cs.sampling_id1 = o.sampling_id
-- JOIN {{ref('observations')}} as o2 ON cs.sampling_id2 = o.sampling_id

