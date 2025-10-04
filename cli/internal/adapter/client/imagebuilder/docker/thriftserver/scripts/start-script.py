from pyspark.sql import SparkSession
import time
from sedona.register.geo_registrator import SedonaRegistrator

spark = SparkSession.builder \
    .appName("Embedding Spark Thrift Server") \
    .config("spark.sql.hive.thriftServer.singleSession", "True") \
    .config("hive.server2.thrift.port", "10001") \
    .config("javax.jdo.option.ConnectionURL",
            "jdbc:derby:;databaseName=metastore_db2;create=true") \
    .enableHiveSupport() \
    .getOrCreate()

SedonaRegistrator.registerAll(spark)
spark.sql("SELECT ST_GeomFromText('POINT(1 1)') AS geom").show(truncate=False)

spark.sql("CREATE SCHEMA IF NOT EXISTS ANALYTICS")
spark.sql(
"""
CREATE EXTERNAL TABLE ANALYTICS.OBSERVATIONS_RAW(
    `Samplingpoint` STRING,
    `Pollutant` INTEGER,
    `Start` TIMESTAMP,
    `End` TIMESTAMP,
    `Value` DECIMAL(38,18),
    `Unit` STRING,
    `AggType` STRING,
    `Validity` INTEGER,
    `Verification` INTEGER,
    `ResultTime` TIMESTAMP,
    `DataCapture` DECIMAL(38,18),
    `FkObservationLog` STRING
) USING PARQUET LOCATION '/opt/spark/spark-warehouse/raw/observations';
"""
)
spark.sql(
    """
    CREATE EXTERNAL TABLE ANALYTICS.BORDERS(
        country STRING,
        geometry GEOMETRY
    ) USING GEOPARQUET LOCATION '/opt/spark/spark-warehouse/raw/borders';
    """
)


sc = spark.sparkContext

sc._gateway.jvm.org.apache.spark.sql.hive.thriftserver \
    .HiveThriftServer2.startWithContext(spark._jsparkSession.sqlContext())
while True:
    time.sleep(5)
