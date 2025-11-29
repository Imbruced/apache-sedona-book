from pyspark.sql import DataFrame, SparkSession
from sedona.spark import SedonaContext
from dataclasses import dataclass
import argparse


@dataclass
class Config:
    output_path: str
    places_path: str


def load_places(sedona: SparkSession, location: str) -> DataFrame:
    places = sedona.\
        read.\
        format("csv").\
        option("delimiter", "\t").\
        load(location).\
        selectExpr(
            "_c0 AS id",
            "_c1 AS category_code",
            "_c2 AS category_name",
            "_c3 AS name",
            "_c4 AS wkt",
        )

    return places

def get_places_by_category(
        places: DataFrame,
        category: str
) -> DataFrame:
    return places.\
        filter(f"category_name = '{category}'").\
        selectExpr(
        "id",
        """ST_Transform(
            ST_GeomFromWKT(wkt),
            'EPSG:4326',
            'EPSG:2180'
            ) AS geometry"""
    )

def get_atm_within_distance_to_restaurant(
        sedona: SparkSession,
        atms: DataFrame,
        restaurants: DataFrame
) -> DataFrame:
    atms.createOrReplaceTempView("atms")
    restaurants.createOrReplaceTempView("restaurants")

    sedona.sql(f"""
     SELECT
        a.id AS atm_id,
        r.id AS restaurant_id,
        a.geometry AS geometry
    FROM atms a
    JOIN restaurants r ON ST_DWithin(a.geometry, r.geometry, 500)
    """).createOrReplaceTempView("nearby_atms_and_restaurants")

    number_of_restaurants = sedona.sql(f"""
        SELECT
            atm_id,
            FIRST(geometry) AS geometry,
            COUNT(restaurant_id) AS number_of_restaurants
        FROM nearby_atms_and_restaurants
        GROUP BY atm_id
    """)

    number_of_restaurants.show()

    return number_of_restaurants


def process_places(sedona: SparkSession, places_location: str, output_path: str) -> None:
    atms = load_places(sedona, places_location). \
        transform(lambda df: get_places_by_category(df, "atm"))

    restaurants = load_places(sedona, places_location). \
        transform(lambda df: get_places_by_category(df, "restaurant"))

    number_of_restaurants = get_atm_within_distance_to_restaurant(sedona, atms, restaurants)

    number_of_restaurants.write. \
        format("parquet"). \
        mode("overwrite"). \
        save(output_path)


def run():
    parser = argparse.ArgumentParser(description="Sedona sample application")
    parser.add_argument('--places_location', type=str, required=True, help='Location of the places CSV file')
    parser.add_argument('--output_path', type=str, required=True, help='Location where to save processed data')

    args = parser.parse_args()

    places_location = args.places_location

    config = SedonaContext.builder()

    sedona = SedonaContext.create(config.getOrCreate())
    sedona.sparkContext.setLogLevel("ERROR")

    output_path = args.output_path
    process_places(sedona, places_location, output_path)


if __name__ == "__main__":
    run()
