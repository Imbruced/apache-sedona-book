import sys

import sedona.spark as s

CATALOG_NAME = "sedona_catalog"
bucket_name = "apache-sedona-book"

(processing_date, input_database, output_database) = sys.argv[1:4]

config = s.SedonaContext.builder() \
    .getOrCreate()

sedona = s.SedonaContext.create(config)

risk_score = sedona.table(f"{CATALOG_NAME}.{input_database}.nl_road_risk_score").\
    selectExpr("ST_GeomFromEWKB(geometry) AS geometry", "RISK_SCORE").\
    filter("RISK_SCORE IS NOT NULL")

risk_score_count = risk_score.count()

assert risk_score_count > 100, "Quality check failed: Risk score count is greater than 100"
assert risk_score_count < 200, "Quality check failed: Risk score count is less than 200"
assert risk_score.selectExpr("ST_Area(geometry) AS area")\
            .filter("area <= 0")\
            .count() == 0, "Quality check failed: Invalid area"
assert risk_score.filter("RISK_SCORE > 1.5").count() == 0, "Quality check failed: Invalid risk score"
