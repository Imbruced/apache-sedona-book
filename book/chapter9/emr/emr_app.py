from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Sedona App").getOrCreate()

spark.sql('SELECT ST_POINT(21, 52) AS geom').show()