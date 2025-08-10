from pyspark.sql import SparkSession
from src.app import get_atm_within_distance_to_restaurant
import pytest
from shapely.geometry import Point


def test_get_atm_within_distance_to_restaurant(
        sedona_session: SparkSession
):
    # given
    atms = sedona_session.createDataFrame(
        [
            (1, "ATM A", Point(19.003, 50.003)),
            (2, "ATM B", Point(19.8, 50.1)),
            (3, "ATM C", Point(19.7, 50.2)),
        ],
        ["id", "name", "geometry"]
    ).selectExpr("id", "name", "ST_Transform(geometry, 'EPSG:4326', 'EPSG:2180') AS geometry")

    restaurants = sedona_session.createDataFrame(
        [
            (1, "Restaurant A", Point(19.0, 50.0)),
            (2, "Restaurant B", Point(19.001, 50.001)),
            (3, "Restaurant C", Point(19.002, 50.002)),
        ],
        ["id", "name", "geometry"]
    ).selectExpr("id", "name", "ST_Transform(geometry, 'EPSG:4326', 'EPSG:2180') AS geometry")

    # when
    result = get_atm_within_distance_to_restaurant(
        sedona=sedona_session,
        atms=atms,
        restaurants=restaurants
    )

    # then
    values = result.collect()
    assert len(values) == 1
    assert values[0].atm_id == 1
    assert values[0].number_of_restaurants == 3
    assert round(values[0].geometry.x, 3) == 500214.923
    assert round(values[0].geometry.y, 3) == 237301.911
