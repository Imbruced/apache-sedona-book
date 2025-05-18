mc alias set sedona http://localhost:9000 sedona sedona_password
mc mb sedona/apache-sedona-book
mc cp /app/sources/ sedona/apache-sedona-book/ --recursive