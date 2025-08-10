import pytest
from pyspark.sql import SparkSession
from sedona.spark import SedonaContext


@pytest.fixture
def sedona_session() -> SparkSession:
    additional_packages = [
        'org.apache.sedona:sedona-spark-3.5_2.12:1.7.2',
        'org.datasyslab:geotools-wrapper:1.7.2-28.5',
    ]

    config = SedonaContext.builder().config("spark.jars.packages", ",".join(additional_packages))

    sedona = SedonaContext.create(config.getOrCreate())
    sedona.sparkContext.setLogLevel("ERROR")

    return sedona