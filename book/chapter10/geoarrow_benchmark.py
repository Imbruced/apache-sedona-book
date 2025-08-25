import sys
import threading
import time
import psutil
import os
from sedona.spark import SedonaContext
import geopandas as gpd
from sedona.spark import dataframe_to_arrow


bucket_name = os.environ.get("SEDONA_SOURCE_BUCKET", "apache-sedona-book")


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
        "spark.driver.memory": "12G",
        "spark.executor.memory": "16G",
        "spark.jars.packages": ",".join(additional_packages),
        "spark.driver.maxResultSize": "6G",
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
    df = sedona.\
        read.\
        format("geoparquet"). \
        load(f"s3a://{bucket_name}/source_data/optimizations/{data_size}")

    df.printSchema()

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
            gdf = convert_using_arrow(df)
            times.append(time.time() - start)
        else:
            gdf = convert_using_non_arrow(df)
            times.append(time.time() - start)
    print(f"Average time for {data_size} data size: {sum(times) / len(times):.4f} seconds")

    # Simulate workload
if __name__ == "__main__":
    main()
    time.sleep(10)