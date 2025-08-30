import sys

import pyspark.sql as sql
import pyspark.sql.functions as f
import sedona.spark as s

CATALOG_NAME = "sedona_catalog"
bucket_name = "apache-sedona-book"

def normalize_column(column_name: str, wage: float) -> callable:
    def transform(df: sql.DataFrame) -> sql.DataFrame:
        max_value = df.selectExpr(f"max({column_name})").collect()[0][0]
        min_value = df.selectExpr(f"min({column_name})").collect()[0][0]

        max_value = 0 if not max_value else max_value
        min_value = 0 if not min_value else min_value

        column_expression = (f.col(column_name) - min_value) / (max_value - min_value)

        if max_value is None:
            column_expression = f.lit(None)

        return df \
            .withColumn(column_name, column_expression) \
            .withColumn(column_name, wage * f.coalesce(f.col(column_name), f.lit(0)))

    return transform


def add_number_of_buildings(df: sql.DataFrame) -> sql.DataFrame:
    buildings = sedona.table(f"{CATALOG_NAME}.{input_database}.nl_buildings").\
        selectExpr("ST_GeomFromEWKB(geometry) AS geometry")

    number_of_buildings = df.alias("h") \
        .join(buildings.alias("b"), f.expr("ST_CONTAINS(h.geometry, ST_CENTROID(b.geometry))")) \
        .groupBy("h.h3") \
        .count() \
        .selectExpr("h.h3", "count AS res_buildings")

    number_of_buildings_normalized = number_of_buildings \
        .transform(normalize_column("res_buildings", 0.3)) \
        .select("h3", "res_buildings")

    return df.join(number_of_buildings_normalized, "h3", how="left")


def normalize_speed_limit(df: sql.DataFrame) -> sql.DataFrame:
    return df \
        .transform(normalize_column("speed_limit", 0.3))


def enrich_with_flood_map(df: sql.DataFrame) -> sql.DataFrame:
    flood_tiles = sedona.table(f"{CATALOG_NAME}.{input_database}.nl_flood_map").\
        selectExpr("RS_FromGeoTiff(rast) AS rast", "event")

    hex_flood = df \
        .alias("t1") \
        .join(flood_tiles.alias("t2"), f.expr("ST_OVERLAPS(RS_ENVELOPE(t2.rast), t1.geometry) ")) \
        .select("t1.h3", "t1.geometry", "t2.rast", "t2.event") \
        .withColumn("flood_point", f.expr("RS_ZonalStats(rast, geometry, 'count')")) \
        .groupBy("h3", "event") \
        .count() \
        .selectExpr("h3", "event", "count AS flood_point_cnt")

    hex_flood.createOrReplaceTempView("hex_flood")

    pivot = sedona.sql(
        """
        SELECT * FROM hex_flood
        PIVOT (
            SUM(flood_point_cnt) AS a
            FOR event IN ('10' AS ten_flood_point_cnt,'20' as twenty_flood_point_cnt,'30' as thirty_flood_point_cnt,'40' as fourty_flood_point_cnt,'50' as fifty_flood_point_cnt,'75' as seventyfive_flood_point_cnt,'100' as one_hundred_flood_point_cnt,'200' as two_hundred_flood_point_cnt,'500' as five_hundred_flood_point_cnt)
        )
        """
    )

    normalized_pivot = pivot \
        .transform(normalize_column("ten_flood_point_cnt", 0.4)) \
        .transform(normalize_column("twenty_flood_point_cnt", 0.3)) \
        .transform(normalize_column("thirty_flood_point_cnt", 0.2)) \
        .transform(normalize_column("fourty_flood_point_cnt", 0.31)) \
        .transform(normalize_column("fifty_flood_point_cnt", 0.09)) \
        .transform(normalize_column("seventyfive_flood_point_cnt", 0.08)) \
        .transform(normalize_column("one_hundred_flood_point_cnt", 0.07)) \
        .transform(normalize_column("two_hundred_flood_point_cnt", 0.06)) \
        .transform(normalize_column("five_hundred_flood_point_cnt", 0.05))

    return df.join(normalized_pivot, "h3", how="left")


(processing_date, input_database, output_database) = sys.argv[1:4]

config = s.SedonaContext.builder() \
    .getOrCreate()

sedona = s.SedonaContext.create(config)
sedona.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

sedona.table(f"{CATALOG_NAME}.{input_database}.nl_transportation_hex_bins") \
    .withColumn("geometry", f.expr("ST_GeomFromEWKB(geometry)")) \
    .transform(add_number_of_buildings) \
    .transform(normalize_speed_limit) \
    .transform(enrich_with_flood_map) \
    .select(
        "h3",
        "geometry",
        (f.col("res_buildings") +
         f.col("speed_limit") +
         f.col("ten_flood_point_cnt") +
         f.col("twenty_flood_point_cnt") +
         f.col("thirty_flood_point_cnt") +
         f.col("fourty_flood_point_cnt") +
         f.col("fifty_flood_point_cnt") +
         f.col("seventyfive_flood_point_cnt") +
         f.col("one_hundred_flood_point_cnt") +
         f.col("two_hundred_flood_point_cnt") +
         f.col("five_hundred_flood_point_cnt")).alias("risk_score")
    ).createOrReplaceTempView("risk_score")

sedona.sql(
    f"""
    INSERT OVERWRITE {CATALOG_NAME}.{output_database}.nl_road_risk_score
    SELECT H3, ST_AsEWKB(GEOMETRY) AS GEOMETRY, RISK_SCORE, CAST('{processing_date}' AS DATE)
    FROM risk_score
    """
)
