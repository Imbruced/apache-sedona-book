from pyspark.sql import SparkSession
import time
import sedona.spark as s

config = (
    s.SedonaContext.builder() \
        .appName("Embedding Spark Thrift Server") \
        .config("spark.sql.hive.thriftServer.singleSession", "True") \
        .config("hive.server2.thrift.port", "10001") \
        .config("javax.jdo.option.ConnectionURL",
                "jdbc:derby:;databaseName=metastore_db2;create=true") \
        .enableHiveSupport() \
        .getOrCreate()
)

sedona = s.SedonaContext.create(config)

sedona.sql("SELECT ST_GeomFromText('POINT(1 1)') AS geom").show(truncate=False)

sedona.sql("CREATE SCHEMA IF NOT EXISTS ANALYTICS")
sedona.sql(
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
sedona.sql(
    """
    CREATE EXTERNAL TABLE ANALYTICS.BORDERS(
        country STRING,
        geometry GEOMETRY
    ) USING GEOPARQUET LOCATION '/opt/spark/spark-warehouse/raw/borders';
    """
)


sc = sedona.sparkContext

sc._gateway.jvm.org.apache.spark.sql.hive.thriftserver \
    .HiveThriftServer2.startWithContext(sedona._jsparkSession.sqlContext())
while True:
    time.sleep(5)
