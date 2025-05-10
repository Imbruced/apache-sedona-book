mc alias set sedona http://localhost:9000 sedona sedona_password
mc mb sedona/sedona
mc cp /app/sources/ sedona/sedona/ --recursive