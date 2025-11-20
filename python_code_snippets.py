# P1 22
from sedona.spark import SedonaContext

additional_packages = [
    "org.apache.sedona:sedona-spark-3.5_2.12:1.7.2",
    "org.datasyslab:geotools-wrapper:1.7.2-28."
]

config = SedonaContext.builder() \
    .config("spark.jars.packages", ",".join(additional_packages))

sedona = SedonaContext.create(config.getOrCreate())


# P1 23

def load_places(sedona: SparkSession, location: str) -> DataFrame:
    places = sedona \
        .read \
        .format("csv") \
        .option("delimiter", "\t") \
        .load(location) \
        .selectExpr(
            "_c0 AS id",
            "_c1 AS category_code",
            "_c2 AS category_name",
            "_c3 AS name",
            "_c4 AS wkt",
        )

    return places


# P1 23
def get_places_by_category(places: DataFrame, category: str) -> DataFrame:
    return places \
        .filter(f"category_name = '{category}'") \
        .selectExpr(
            "id",
            "ST_Transform(ST_GeomFromWKT(wkt), 'EPSG:4326', 'EPSG:2180') AS geometry"
        )


# P1 24
def get_atm_within_distance_to_restaurant(
        sedona: SparkSession,
        atms: DataFrame,
        restaurants: DataFrame
) -> DataFrame:
    atms.createOrReplaceTempView("atms")

    restaurants.createOrReplaceTempView("restaurants")

    sedona.sql("Spatial Join SQL") \
        .createOrReplaceTempView("nearby_atms_and_restaurants")

    return sedona.sql("aggregate SQL")

# P1 24
number_of_restaurants.write \
    .format("parquet") \
    .mode("overwrite") \
    .save(output_path)


# P1 25
@pytest.fixture
def sedona_session() -> SparkSession:
    # create and return Sedona context here
    return sedona

# P1 25
from shapely.geometry import Point
from sedona.spark.sql.st_functions import ST_Transform
from pyspark.sql.functions import col, lit

atms = sedona.createDataFrame(
    [
        (1, "ATM A", Point(19.003, 50.003)),
        (2, "ATM B", Point(19.8, 50.1)),
        (3, "ATM C", Point(19.7, 50.2))
    ],
    ["id", "name", "geometry"]
).select(
    "id",
    "name",
    ST_Transform(
        col("geometry"),
        lit("EPSG:4326"),
        lit("EPSG:2180")
    ).alias("geometry")
)

# P1 25
result = get_atm_within_distance_to_restaurant(
    sedona=sedona_session,
    atms=atms,
    restaurants=restaurants
)

# P1 26
values = result.collect()

assert len(values) == 1
assert values[0].atm_id == 1
assert values[0].number_of_restaurants == 3
assert round(values[0].geometry.x, 3) == 500214.923
assert round(values[0].geometry.y, 3) == 237301.911

# P1 29
from sedona.spark import *

config = SedonaContext \
    .builder() \
    .master("spark://localhost:7077") \
    .getOrCreate()

sedona = SedonaContext.create(config)

# P1 30
cities_df = sedona \
    .createDataFrame(
        [
            ("San Francisco", -122.4191, 37.7749),
            ("New York", -74.0060, 40.7128),
            ("Austin", -97.7431, 30.2672)
        ],
        ["city", "longitude", "latitude"]
    )

cities_df.show()

# P1 32
cities_df = sedona \
    .sql("""
        SELECT 
            *,
            ST_Point(longitude, latitude) AS geometry
        FROM cities
    """)

cities_df.show(truncate=False)

# P1 33
buffer_df = sedona \
    .sql("""
        SELECT 
            city,
            ST_Buffer(geometry, 1000, true) AS geometry
        FROM cities
    """)

buffer_df.show()

# P1 34
from sedona.sql.st_functions import ST_MakeLine
from pyspark.sql.functions import collect_list, col

route_df = cities_df.select(
    ST_MakeLine(collect_list(col("geometry"))).alias("geometry")
)

route_df.show(truncate=False)

# P1 42
import sedona.sql.functions as sf

sedona.read \
    .format("csv") \
    .option("header", "true") \
    .option("quote", '"') \
    .load(path) \
    .withColumn("wkt", sf.ST_GeomFromText("wkt")) \
    .show()

# P1 43
sedona.read \
    .format("shapefile") \
    .load(path) \
    .select("osm_id", "geometry") \
    .show(5)

# P1 45
sedona.read \
    .format("geojson") \
    .option("multiLine", "true") \
    .load(path) \
    .show(5)

# P1 45
sedona.read \
    .format("geojson") \
    .option("multiLine", "true") \
    .load(path) \
    .selectExpr("explode(features) as features") \
    .select("features.geometry", "features.properties.osm_id") \
    .show(5)

# P1 46
sedona.read \
    .format("geojson") \
    .load(path) \
    .selectExpr("geometry", "properties.*") \
    .show(5)

# P1 47
sedona.read \
    .format("geopackage") \
    .option("showMetadata", "true") \
    .load(f"s3a://{bucket_name}/source_data/vector/geopackage") \
    .select("table_name", "data_type", "srs_id") \
    .show(5)

# P1 47
sedona.read \
    .format("geopackage") \
    .option("tableName", "gis_osm_roads_free_1") \
    .load(f"s3a://{bucket_name}/source_data/vector/geopackage") \
    .select("osm_id", "geom") \
    .show(5)

# P1 48
sedona \
    .read \
    .format("geoparquet") \
    .load(path) \
    .show(5)

# P1 49
sedona \
    .read \
    .format("geoparquet") \
    .load(path) \
    .withColumn("geohash", f.expr("ST_GeoHash(geometry, 2)")) \
    .orderBy("geohash") \
    .write \
    .format("geoparquet") \
    .save("target_path")

# P1 50
envelope_str = "-123.425407, 35.749839, -118.763583, 41.806623"

df = sedona \
    .read \
    .format("geoparquet") \
    .load(path) \
    .where(f"ST_Within(geometry, ST_PolygonFromEnvelope({envelope_str}))") \
    .selectExpr("brand.names.primary as name") \
    .groupBy("name") \
    .count()

# P1 53
geotiff_df = sedona \
    .read \
    .format("binaryFile") \
    .load(path)

# P1 53
geotiff_df \
    .selectExpr("RS_FromGeoTiff(content) AS raster") \
    .createOrReplaceTempView("japan")

# P1 55
config = SedonaContext \
    .builder() \
    .config("spark.jars.packages", 'org.postgresql:postgresql:42.7.4') \
    .getOrCreate()

sedona = SedonaContext.create(config)

postgresql_url = "jdbc:postgresql://localhost:5432/sedona"

# P1 55/56
table_name = "points"

df = sedona \
    .read \
    .format("jdbc") \
    .option("url", postgresql_url) \
    .option("user", "sedona") \
    .option("password", "sedona") \
    .option("dbtable", "points") \
    .option("driver", "org.postgresql.Driver") \
    .load()

df.show()

# P1 56
df.selectExpr(
    "name",
    "ST_GeomFromEWKB(location) AS geom"
).show()

# P1 56/57
mysql_url = f"jdbc:mysql://localhost:3306/{database_name}"

df = sedona \
    .read \
    .format("jdbc") \
    .option("url", mysql_url) \
    .option("user", user_name) \
    .option("password", password) \
    .option("dbtable", "points") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .load()

df.show()

# P1 57
df.selectExpr(
    "name",
    "ST_GeomFromMySQL(location) AS geom"
).show(3, False)

# P1 57
df = sedona \
    .read \
    .option("database", "sedona") \
    .option("collection", "points") \
    .format("mongodb") \
    .load()

# P1 58
import pyspark.sql.functions as f

df.withColumn("location", f.to_json(f.col("location"))) \
    .selectExpr("name", "ST_GeomFromGeoJSON(location) AS geom") \
    .show(2, False)

# P1 60
df = sedona \
    .read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sedona-debezium.public.points") \
    .load()

# P1 61
import pyspark.sql.types as t

data = t.StructType([
    t.StructField("name", t.StringType(), True),
    t.StructField("location", t.StructType([
        t.StructField("srid", t.IntegerType()),
        t.StructField("wkb", t.BinaryType())])
    )
])

before = t.StructField("before", data, True)
after = t.StructField("after", data, True)

payload = t.StructField("payload", t.StructType([before, after]) )

schema = t.StructType([payload])

# P1 61
import pyspark.sql.functions as f

geometry_df = df \
    .select(
        f.from_json(f.expr("CAST(value AS STRING)"), schema).alias("data")
    ) \
    .selectExpr(
        "data.payload.after.name as name",
        "data.payload.after.location.wkb as wkb",
        "data.payload.after.location.srid AS srid"
    ) \
    .selectExpr("name", "ST_SetSRID(ST_GeomFromWKB(wkb), srid) AS geom")

# P1 61
geometry_df \
    .withColumn("geohash", f.expr("ST_GeoHash(geom, 5)")) \
    .orderBy("geohash") \
    .write \
    .mode("overwrite") \
    .format("geoparquet") \
    .save("s3a://<your-bucket>/postgis-cdc-batch")

# P1 62
nyx_taxi = sedona \
    .read \
    .format("parquet") \
    .load(path)

# P1 89
spark \
    .table("authors") \
    .join(
        spark.table("books").hint("broadcast"),
        "author_id"
    )

# P1 92
import pyspark.sql.types as t
import pyspark.sql.functions as f

intersects = f.udf(lambda left, right: left.intersects(right), t.BooleanType())

result = points \
    .alias("p") \
    .join(
        lines.alias("l"),
        intersects(f.col("p.geom"), f.col("l.geom"))
    )

# P1 109
area_of_analysis = "POLYGON((-87.9401 41.6445, -87.9401 42.0230,...))"

buildings = sedona \
    .read \
    .format("geoparquet") \
    .load(f"s3a://apache-sedona-book/buildings") \
    .where(f"ST_Intersects(geometry, ST_GeomFromText('{area_of_analysis}'))") \
    .where("class='residential'")

# P1 109/110
roads = sedona \
    .read \
    .format("geoparquet") \
    .load(f"s3a://apache-sedona-book/source_data/us_roads_repartitioned") \
    .where(f"ST_Intersects(geometry, ST_GeomFromText('{area_of_analysis}'))")

noisy_road_classes = [
    "motorway",
    "trunk",
    "primary",
    "secondary",
    "tertiary"
]

noisy_roads = roads.where(
    (
        (
            (f.col("class").isin(noisy_road_classes)) &
            (f.col("subtype") == "road")
        ) |
        (
            (f.col("subtype") == "rail") &
            (f.expr("class IS NULL"))
        )
    )
)

noisy_roads.createOrReplaceTempView("noisy_roads")

# P1 110
places = sedona \
    .read \
    .format("geoparquet") \
    .load(f"s3a://apache-sedona-book/source_data/us_places") \
    .where(f"ST_Intersects(geom, ST_GeomFromText('{area_of_analysis}'))")

categories_raw = sedona \
    .sql("""
        SELECT 
            category_id
        FROM categories
        WHERE category_name = 'Grocery Store'
     """
    ).collect()

categories = [c[0] for c in categories_raw]

places \
    .where(f.arrays_overlap("fsq_category_ids", f.lit(categories))) \
    .select("fsq_place_id", "geom") \
    .createOrReplaceTempView("grocery_stores")

# P1 120
df = sedona \
    .read \
    .format("binaryFile") \
    .load("/some/path/*.asc")

# P1 122
import itertools

input_raster = [
    [1, 1, 16, 2, 6],
    [2, 3, 12, 16, 17],
    [8, 17, 5, 20, 7],
    [14, 8, 15, 4, 11],
    [10, 13, 19, 6, 9]
]

flatten = list(itertools.chain.from_iterable(input_raster))
array_input = ", ".join([str(number) for number in flatten])

raster_df = sedona \
    .sql(
        f"""
        WITH empty_raster AS (
            SELECT
                RS_MakeEmptyRaster(
                    1, 5, 5, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 4326
                ) AS rast
        )
        SELECT
            RS_MakeRaster(rast, 'D', ARRAY({array_input})) AS rast
        FROM empty_raster
        """
)

# P1 131
matrix = sedona \
    .sql("SELECT RS_AsMatrix(rast) FROM raster") \
    .head()[0]

print(matrix)

# P1 141
from pyspark.sql.functions import input_file_name

swir_channel = sedona \
    .read \
    .format("binaryFile") \
    .load("data/map-algebra/b11_tiles/") \
    .withColumn("file_name", input_file_name()) \
    .selectExpr("RS_FromGeoTiff(content) AS rast", "file_path") \
    .createOrReplaceTempView("swir_raw")

# 166
geotiff_df = sedona \
    .read \
    .format("binaryFile") \
    .load("ID73_S20_W70_RP10_depth.tif") \
    .selectExpr("RS_FromGeoTiff(content) AS rast") \
    .selectExpr("RS_TileExplode(rast, 4096, 4096) AS (x, y, rast)")

# 173
config = s.SedonaContext \
    .builder() \
    .getOrCreate()

sedona = s.SedonaContext.create(config)

# 183/184
import geopandas as gpd
import pyspark.sql.functions as f
from sedona.spark import dataframe_to_arrow

gdf = gpd.GeoDataFrame.from_arrow(dataframe_to_arrow(spatial_df))

ax = gdf.to_crs(epsg=3857) \
    .plot(
        column="type", figsize=(10, 10),
        missing_kwds={
            "color": "lightgrey",
            "edgecolor": "red",
            "label": "Missing values"
        },
        legend=True,
        legend_kwds={"title": "Sedona buildings"}
    )

cx.add_basemap(ax)

# 206
import pyspark.sql.functions as f

buildings_predicted = buildings \
    .selectExpr("RS_FromGeoTiff(content) AS rast")\
    .select(extract_buildings(f.col("rast")).alias("geom"))

# 206
buildings_predicted \
    .selectExpr("EXPLODE(ST_Dump(geom)) AS geometry") \
    .show()

# 209/210
h3_cells = sedona.sql(
    f"""
        WITH h3_cells AS (
            SELECT
                id,
                ST_H3ToGeom(ARRAY(id))[0] AS geom
            LATERAL VIEW EXPLODE(
                ST_H3CellIDs(ST_GeomFromText('{paris_polygon_wkt}'), 8, true)
            ) AS id
        SELECT
            id,
            geom,
            ST_X(ST_Centroid(geom)) AS lon,
            ST_Y(ST_Centroid(geom)) AS lat
        FROM h3_cells
    """
)

# 210
import requests
from shapely.geometry import shape, MultiPolygon

OPEN_ROUTING_URL = "http://localhost:8085"


def walk_time_polygon(
    lon: float,
    lat: float,
    minutes: int
) -> MultiPolygon | None:
    body = {
        "locations": [[lon, lat]],
        "range": [minutes * 60],
        "range_type": "time"
    }

    response = requests.post(
        url=f"{OPEN_ROUTING_URL}/ors/v2/isochrones/foot-walking",
        json=body
    )

    if response.status_code != 200:
        return None

    response_data = response.json()
    features = response_data["features"]

    shapely_polygons = [
        shape(feature["geometry"]) for feature in features
        if feature["geometry"]["type"] == "Polygon"
    ]

    return MultiPolygon(shapely_polygons)

# 211
categories = [
    "restaurant",
    "shopping",
    "bakery",
    "education",
    "school",
    "pharmacy",
    "cafe",
    "theatre",
    "transportation",
    "park",
    "hospital"
]

paris_places \
    .where(f"categories.primary IN {tuple(categories)}") \
    .selectExpr(
        "categories.primary AS category",
        "geometry"
    ) \
    .createOrReplaceTempView("selected_categories")

# 212
feature_df = sedona \
    .table("catchments_count") \
    .groupBy("id", "geom") \
    .pivot("category", categories) \
    .agg(
        f.first("count")
    ) \
    .selectExpr(
        "id",
        "geom",
        "COALESCE(restaurant, 0) AS restaurant",
        "COALESCE(shopping, 0) AS shopping",
        "COALESCE(bakery, 0) AS bakery",
        "COALESCE(education, 0) AS education",
        "COALESCE(school, 0) AS school",
        "COALESCE(pharmacy, 0) AS pharmacy",
        "COALESCE(cafe, 0) AS cafe",
        "COALESCE(theatre, 0) AS theatre",
        "COALESCE(transportation, 0) AS transportation",
        "COALESCE(park, 0) AS park"
    )

# 217
crossings = infrastructure \
    .where("class == 'crossing'") \
    .selectExpr(
        "id",
        "ST_Transform(geometry, 'epsg:4326', 'epsg:3044') AS geometry"
    )

road_classes = (
    'motorway',
    'trunk',
    'primary',
    'secondary',
    'tertiary',
    'residential'
)

enriched_transportation = transportation \
    .where(f"class in {road_classes}") \
    .withColumn(
        "geometry",
        f.expr("ST_Transform(geometry, 'epsg:4326', 'epsg:3044')")
    ) \
    .withColumn("width", widths_mapping_expr[f.col("class")]) \
    .withColumn(
        "max_speed",
        map_speed_limit(f.col("speed_limits"), f.col("class"))
    ) \
    .select(
        "id",
        "geometry",
        "width",
        "max_speed",
        is_bridge,
        is_tunnel,
        is_under_construction,
        get_average_curvature("geometry").alias("curvature"),
    "quality")

# 221
typical_widths = {
    "motorway": 25,
    "trunk": 20,
    "primary": 12,
    "secondary": 10,
    "tertiary": 8,
    "residential": 6,
    "service": 5

}
widths_mapping_expr = f.create_map(
    [f.lit(x) for pair in typical_widths.items() for x in pair]
)

# 221
roads_with_accidents = enriched_transportation \
    .alias("t") \
    .join(
        accidents.alias("a"),
        on=f.expr("ST_DWithin(t.geometry, a.geometry, t.width)")
    ) \
    .selectExpr(
        "t.*",
        "a.lighting_condition",
        "a.accident_category",
        "a.promiles"
    )

# 222
roads_feature_values = roads_with_accidents \
    .alias("ra") \
    .join(
        crossings.alias("c"),
        on=f.expr("ST_KNN(ra.geometry, c.geometry, 1)")
    ) \
    .selectExpr(
        "ra.id",
        "ra.geometry",
        "ra.max_speed AS ms",
        "ra.is_bridge AS is_b",
        "ra.is_tunnel AS is_t",
        "ra.is_under_construction AS is_uc",
        "ROUND(ra.curvature, 3) AS c",
        "ra.lighting_condition AS lc",
        "ra.accident_category AS ac",
        "ROUND(ST_Distance(c.geometry, ra.geometry), 2) AS distance",
        "ra.promiles",
        "ra.quality"
    )

# 223
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

window_spec = Window.partitionBy("id").orderBy(f.desc("count"))
similar_size_buckets = Window.partitionBy("ac").orderBy("id")

roads_feature_values_ranked = roads_feature_values \
    .groupBy("id", "ac", "lc", "promiles") \
    .agg(
        f.col("id"),
        f.count("*").alias("count"),
        f.first("ms").alias("ms"),
        f.first("is_b").alias("is_b"),
        f.first("is_t").alias("is_t"),
        f.first("is_uc").alias("is_uc"),
        f.first("c").alias("c"),
        f.first("distance").alias("distance"),
        f.first("quality").alias("quality")
    ) \
    .withColumn("rank", row_number().over(window_spec)) \
    .where("rank == 1") \
    .withColumn("bucket_size", row_number().over(similar_size_buckets)) \
    .where("bucket_size < 1000") \
    .drop("rank", "bucket_size")

# 223/224

from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    StringIndexer, OneHotEncoder, VectorAssembler, MinMaxScaler
)
from pyspark.sql.functions import col

# Convert the boolean fields to 0, 1 integer values
roads_feature_values_transformed = roads_feature_values_ranked \
    .withColumn("is_b", col("is_b").cast("int")) \
    .withColumn("is_t", col("is_t").cast("int")) \
    .withColumn("is_uc", col("is_uc").cast("int"))


# 240
sedona \
    .read \
    .format("geoparquet.metadata") \
    .load(path) \
    .show()

# 270
from sedona.spark import SedonaContext

config = SedonaContext \
    .builder() \
    .appName('WherobotsExample') \
    .getOrCreate()

sedona = SedonaContext.create(config)

# 271
complex_buildings = buildings \
    .selectExpr("id", "class", "geometry") \
    .where("ST_NPoints(geometry) > 30")

# 285
buildings_water = buildings_spatially_filtered.alias("b") \
    .join(
        water_pretransformed.alias("w"),
        f.expr("ST_Intersects(w.geometry, b.geometry)")
    ) \
    .selectExpr(
        "b.id",
        "b.geometry AS b_geometry",
        "w.subtype"
    ) \
    .groupBy("id", "subtype") \
    .agg(
        f.expr("COUNT(*) AS count"),
        f.expr("FIRST(b_geometry) AS geometry")
    )

# 285
most_common_water_type = buildings_water \
    withColumn("rank", f.expr("RANK() OVER (PARTITION BY id ORDER BY count)"))

# 289
from sedona.spark import SedonaContext

sedona_spark = "org.apache.sedona:sedona-spark-3.5_2.12:1.7.2"
geotools = "org.datasyslab:geotools-wrapper:1.7.2-28.5"

config = SedonaContext.builder() \
    .config("spark.jars.packages", f"{sedona_spark},{geotools}")

sedona = SedonaContext.create(config.getOrCreate())

# 293
import pyspark.sql.functions as f

left.alias("l") \
    .join(
        f.broadcast(right.alias("r")),
        f.expr("ST_Intersects(l.geometry, r.geometry)")
    ) \
    .select("l.id", "l.geometry")