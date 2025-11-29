from sedona.spark import SedonaContext

config = SedonaContext.builder()

sedona = SedonaContext.create(config.getOrCreate())

sedona.sql('SELECT ST_POINT(21, 52) AS geom').show()