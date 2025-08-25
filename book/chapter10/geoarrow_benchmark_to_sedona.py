import sys
import threading
import time
import psutil
import os
from sedona.spark import SedonaContext
import geopandas as gpd
from sedona.sql.types import GeometryType
from sedona.spark.geoarrow import create_spatial_dataframe

from pyspark.sql.types import (
    StructType, StructField, StringType, FloatType, IntegerType, DoubleType,
    BooleanType, ArrayType, MapType
)

schema = StructType([
    StructField("id", StringType(), True),
    StructField("geometry", GeometryType(), True),  # Replace with appropriate type if using geospatial extensions
    StructField("bbox", StructType([
        StructField("xmin", FloatType(), True),
        StructField("xmax", FloatType(), True),
        StructField("ymin", FloatType(), True),
        StructField("ymax", FloatType(), True),
    ]), True),
    StructField("theme", StringType(), True),
    StructField("type", StringType(), True),
    StructField("version", IntegerType(), True),
    StructField("sources", ArrayType(
        StructType([
            StructField("property", StringType(), True),
            StructField("dataset", StringType(), True),
            StructField("record_id", StringType(), True),
            StructField("update_time", StringType(), True),
            StructField("confidence", DoubleType(), True),
        ])
    ), True),
    StructField("level", FloatType(), True),
    StructField("subtype", StringType(), True),
    StructField("class", StringType(), True),
    StructField("height", DoubleType(), True),
    StructField("names", StructType([
        StructField("primary", StringType(), True),
        # StructField("common", MapType(StringType(), StringType(), True), True),
        StructField("rules", ArrayType(
            StructType([
                StructField("variant", StringType(), True),
                StructField("language", StringType(), True),
                StructField("value", StringType(), True),
                StructField("between", ArrayType(DoubleType(), True), True),
                StructField("side", StringType(), True),
            ])
        ), True)
    ]), True),
    StructField("has_parts", BooleanType(), True),
    StructField("is_underground", BooleanType(), True),
    StructField("num_floors", FloatType(), True),
    StructField("num_floors_underground", FloatType(), True),
    StructField("min_height", DoubleType(), True),
    StructField("min_floor", FloatType(), True),
    StructField("facade_color", StringType(), True),
    StructField("facade_material", StringType(), True),
    StructField("roof_material", StringType(), True),
    StructField("roof_shape", StringType(), True),
    StructField("roof_direction", DoubleType(), True),
    StructField("roof_orientation", StringType(), True),
    StructField("roof_color", StringType(), True),
    StructField("roof_height", DoubleType(), True),
])


def monitor_memory(interval=1.0):
    process = psutil.Process(os.getpid())
    peak_rss = 0
    while True:
        rss = process.memory_info().rss
        if rss > peak_rss:
            peak_rss = rss
        print(f"[Monitor] Current RSS: {rss / (1024**2):.2f} MB | Peak: {peak_rss / (1024**2):.2f} MB")
        time.sleep(interval)

# Start monitoring in background
monitor_thread = threading.Thread(target=monitor_memory, args=(1,), daemon=True)
monitor_thread.start()

sizes = {
    "small": "10k",
    "medium": "500k",
    "large": "10m",
}

def convert_using_arrow(df):
    return gpd.GeoDataFrame.from_arrow(
        dataframe_to_arrow(df)
    )

def convert_using_non_arrow(df):
    return gpd.GeoDataFrame(
        df.toPandas(),
        geometry="geometry"
    )

def main():
    additional_packages = [
        'org.apache.sedona:sedona-spark-3.5_2.12:1.7.2',
        'org.datasyslab:geotools-wrapper:1.7.2-28.5',
    ]

    config_params =  {
        "spark.driver.memory": "30G",
        "spark.executor.memory": "16G",
        "spark.jars.packages": ",".join(additional_packages),
        "spark.driver.maxResultSize": "10G",
        "spark.network.timeout": "1000s",
        "spark.rpc.askTimeout": "1000s",
        "spark.executor.heartbeatInterval": "5s",
    }

    config = SedonaContext.builder()

    for key, value in config_params.items():
        config = config.config(key, value)

    sedona = SedonaContext.create(config.getOrCreate())
    sedona.sparkContext.setLogLevel("ERROR")

    # get first argument from command    line
    data_size = sys.argv[1]
    if data_size not in sizes:
        raise ValueError(f"Invalid data size: {data_size}. Choose from {list(sizes.keys())}.")

    data_size = sizes[data_size]
    gdf = gpd.read_parquet(f"data/buildings/{data_size}/")

    times = []
    tries = int(sys.argv[2])
    use_geoarrow = sys.argv[3].lower() == "true"
    if use_geoarrow:
        print("Using GeoArrow conversion")
    else:
        print("Using non-GeoArrow conversion")

    for _ in range(tries):
        start = time.time()
        if use_geoarrow:
            df = create_spatial_dataframe(sedona, gdf)

            times.append(time.time() - start)
        else:
            df = sedona.createDataFrame(gdf, schema=schema)
            times.append(time.time() - start)
    print(f"Average time for {data_size} data size: {sum(times) / len(times):.4f} seconds")

    # Simulate workload
if __name__ == "__main__":
    main()
    time.sleep(10)