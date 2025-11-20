-- P1 24

SELECT
    a.id AS atm_id,
    r.id AS restaurant_id,
    a.geometry AS geometry
FROM atms a
JOIN restaurants r ON ST_DWithin(a.geometry, r.geometry, 500)

-- P1 24

SELECT
    atm_id,
    FIRST (geometry) AS geometry,
    COUNT (restaurant_id) AS number_of_restaurants
FROM nearby_atms_and_restaurants
GROUP BY atm_id


-- P1 33
SELECT
    ST_Makeline(collect_list(geometry)) AS geometry
FROM cities

-- P1 54
WITH algebra_result AS (
    SELECT
        RS_MapAlgebra(
            tile,
            'D',
            'out = (rast[1] - rast[0]) / (rast[1] + rast[0]);'
        ) AS raster,
        ST_SetSRID(ST_GeomFromText('{wkt}'), 32653) AS geom
    FROM tiles
),
clipped AS (
    SELECT
        RS_Clip(raster, 1, geom) AS raster
    FROM algebra_result
    WHERE RS_Intersects(geom, raster)
)
SELECT raster
FROM clipped

-- P1 63
SELECT
    *
FROM taxi
WHERE ST_Within(dropoff_geom, ST_GeomFromText('{polygon_wkt}'))
  AND ST_Within(pickup_geom, ST_GeomFromText('{polygon_wkt}'))
  AND total_amount > 0

-- P1 64
WITH h3_index AS (
    SELECT
        ST_H3CellIDs(dropoff_geom, 8, true)[0] AS h3_id
    FROM taxi_cleaned
)
SELECT
    h3_id,
   count(h3_id) AS cnt,
   ST_H3ToGeom(array(h3_id))[0] AS geom
FROM h3_index
GROUP BY h3_id
ORDER BY count(h3_id) DESC

-- P1 65
SELECT
    ST_H3CellIDs(pickup_geom, 8, true)[0] AS h3_pickup_id,
    ST_H3CellIDs(dropoff_geom, 8, true)[0] AS h3_dropoff_id
FROM taxi_cleaned

-- P1 65/66
SELECT
    CASE
        WHEN h3_pickup_id > h3_dropoff_id
            THEN CONCAT(h3_dropoff_id, ' ', h3_pickup_id)
            ELSE CONCAT(h3_pickup_id, ' ', h3_dropoff_id)
    END AS id,
    h3_pickup_id,
    h3_dropoff_id
FROM h3_indexes

-- P1 66
SELECT
    id,
    count(id) AS cnt,
    first(h3_pickup_id) AS h3_pickup_id,
    first(h3_dropoff_id) AS h3_dropoff_id
FROM indexed
GROUP BY id

-- P1 67
SELECT
    id,
    count(id) AS cnt,
    first(h3_pickup_id) AS h3_pickup_id,
    first(h3_dropoff_id) AS h3_dropoff_id
FROM indexed
GROUP BY id

-- P1 86
SELECT
    osm_id as id,
    ST_StartPoint(geometry) AS geom
FROM roads
UNION ALL
SELECT
    osm_id AS id,
    ST_EndPoint(geometry) AS geom
FROM roads

-- P1 87
SELECT
    ST_ConvexHull(ST_Union_Aggr(geometry))
FROM roads
WHERE (name = 'Phố Giảng Võ' OR name = 'Phố Kim Mã') AND fclass = 'primary'

-- P1 87
SELECT DISTINCT name
FROM roads
WHERE ST_Intersects(geometry, (
    SELECT
        ST_Transform(
            ST_Buffer(
                ST_Transform(geom, 'EPSG:3405'),
                500
            ),
            'EPSG:4326'
        ) AS geom
    FROM convex_hull
))

-- P1 88
SELECT
    DISTINCT name
FROM roads
WHERE ST_DWithin(geometry, (SELECT geom FROM convex_hull), 500, true)

-- P1 93
SELECT
    s.name,
    c.name
FROM city AS c
JOIN superhero AS s ON ST_Contains(c.geom, s.geom)

-- P1 102
SELECT
    df1.*
FROM df1, df2
WHERE ST_DistanceSpheroid(df1.geom, df2.geom) < 100

-- P1 102
SELECT
    df1.*
FROM df1
JOIN df2 ON  ST_DistanceSpheroid(df1.geom, df2.geom) < 100

-- P1 103
SELECT
    df1.*
FROM df1, df2
WHERE ST_DWithin(df1.geom, df2.geom, 10.0)

-- P1 103
SELECT
    df1.*
FROM df1
JOIN df2 ON ST_DWithin(df1.geom, df2.geom, 10.0)

-- P1 103
SELECT
    left.*
FROM points AS p
JOIN polygons AS pl ON ST_INTERSECTS(p.geom, pl.geom)

-- P1 110/111
SELECT
    b.id,
    ST_DistanceSpheroid(b.geometry, n.geometry)
FROM buildings AS b
JOIN noisy_roads as n ON ST_KNN(b.geometry, n.geometry, 1)

-- P1 111
WITH grocery_stores_nearby AS (
    SELECT
        b.id AS building_id,
        g.fsq_place_id AS g_id
    FROM buildings AS b
    JOIN grocery_stores AS g ON ST_DWithin(g.geom, b.geometry, 500, true)
)
SELECT
    building_id AS id,
    count(g_id) AS number_of_grocery_stores
FROM grocery_stores_nearby
GROUP BY id

-- P1 111
SELECT
    b.id AS building_id,
    p.fsq_place_id AS poi_id,
    p.fsq_category_ids
FROM buildings AS b
JOIN places AS p ON ST_DWithin(p.geom, b.geometry, 300, true)

-- P1 111
SELECT
    building_id,
    poi_id,
    explode(fsq_category_ids) AS category_id
FROM pois_intersected

-- P1 111
SELECT
    building_id AS id,
    count(poi_id) AS number_of_pois,
    category_id
FROM pois_with_categries
GROUP BY id, category_id

-- P1 112
SELECT
    id,
    row_number() OVER (
        PARTITION BY id ORDER BY number_of_pois DESC
    ) as rank,
    category_id
FROM pois_cnt

-- P1 113
SELECT
    id,
    category_id
FROM pois_ranked
WHERE rank <= 3

-- P1 113
SELECT
    id,
    collect_list(category_name) AS category_names
FROM pois_with_categries_resolved
GROUP BY id

-- P1 124
SELECT
    pixels.col.*
FROM raster
LATERAL VIEW EXPLODE(RS_PixelAsCentroids(rast, 1)) pixels

-- P1 124
WITH pixelized AS (
    SELECT
        RS_PixelAsPolygons(rast, 1) AS pixels
    FROM raster
)
SELECT
    ST_Union_Aggr(pixel.geom) AS geom
FROM pixelized
LATERAL VIEW explode(pixels) AS pixel
WHERE pixel.value > 2 and pixel.value < 14

-- P1 134
SELECT
    id,
    ST_Buffer(geom, 20) AS geom,
    "20" AS buffer
FROM properties
UNION ALL
SELECT
    id,
    ST_Buffer(geom, 50) AS geom,
    "50" AS buffer
FROM properties
UNION ALL
SELECT
    id,
    ST_Buffer(geom, 100) AS geom,
    "100" AS buffer
FROM properties

-- P1 149/150
SELECT
    b.id,
    ST_Buffer(
        ST_Intersection(b.geometry, RS_Envelope(rast)),
        -0.00001
    ) AS geometry,
    rast
FROM buildings AS b
JOIN population AS p ON RS_Intersects(geometry, rast)

-- P1 151
SELECT b.id,
       ST_Buffer(
           ST_Intersection(
                ST_Transform(b.geometry, 'epsg:4326', 'epsg:3857'),
                RS_Envelope(rast)
           ),
           -0.00001
       ) AS geom,
       rast,
       risk
FROM buildings AS b
JOIN fire_risk AS p ON RS_Intersects(geometry, rast)

-- P1 153
WITH nearby_buildings AS (
    SELECT
        b1.id AS b1_id,
        b2.id AS b2_id
    FROM buildings AS b1
    JOIN buildings AS b2 ON ST_DWithin(b1.geometry, b2.geometry, 500, true)
)
SELECT
    b1_id AS id,
    count(*) AS density
FROM nearby_buildings
GROUP BY b1_id

-- 164
SELECT
    ST_BufferDistanceNonVectorized(
        geometry,
        0.0001,
        0.0002
    ) AS geom
FROM roads

-- 209/210
