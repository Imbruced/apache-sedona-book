from prefect import flow
import sedona.spark as s
import pyspark.sql.functions as f


@flow
def sedona_flow():
    config = (
        s.SedonaContext.builder() \
            .appName("Sedona") \
            .config("spark.shuffle.partitions", "8") \
            .getOrCreate()
    )

    sedona = s.SedonaContext.create(config)

    df = sedona.sql(
        """
        SELECT 
            ST_GeomFromWKT('POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))') AS geom,
            1 AS id
        UNION ALL
        SELECT 
            ST_GeomFromWKT('POLYGON((1 1, 1 2, 2 2, 2 1, 1 1))') AS geom,
            2 AS id
        UNION ALL
            SELECT ST_GeomFromWKT('POLYGON((2 2, 2 3, 3 3, 3 2, 2 2))') AS geom,
            3 AS id
        """
    )

    transformed = df.withColumn("area", f.expr("ST_Area(geom)"))

    transformed.write.format("parquet").mode("overwrite").save("/opt/prefect/data/sedona_output")
