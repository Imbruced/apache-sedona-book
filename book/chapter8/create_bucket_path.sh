mc alias set sedona http://localhost:9000 sedona sedona_password
mc mb sedona/apache-sedona-book

# Create a "directory" (actually just a prefix)
mc cp /dev/null sedona/apache-sedona-book/data