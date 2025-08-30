import sys

import sedona.spark as s

CATALOG_NAME = "sedona_catalog"

(processing_date, input_database,
 output_database
 ) = sys.argv[1:4]

config = s.SedonaContext.builder() \
    .getOrCreate()

sedona = s.SedonaContext.create(config)

buildings = sedona.table(f"{CATALOG_NAME}.{input_database}.nl_buildings")
buildings_count = buildings.count()

assert buildings_count > 300_000, "Quality check failed: Buildings count is greater than 300k"
assert buildings_count < 400_000, "Quality check failed: Buildings count is less than 400k"

assert buildings.selectExpr("ST_Area(ST_GeomFromEWKB(geometry)) AS area")\
            .filter("area <= 0")\
            .count() == 0, "Quality check failed: Invalid area"
