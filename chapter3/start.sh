docker exec postgis psql -h localhost -U postgis -d postgis -f postgis.sql
docker exec postgis psql -h localhost -U sedona -d sedona -f postgis_ddl.sql

docker exec -i mysql mysql -h localhost -u sedona -p sedona --password=sedona < ./scripts/mysql_ddl.sql

docker exec -it oracle sqlplus sedona/sedona@localhost:1521/FREEPDB1 @oracle_ddl.sql

curl --location 'http://localhost:8083/connectors' \
   --header 'Accept: application/json' \
   --header 'Content-Type: application/json' \
   --data '{
   "name": "sedona-postgis",
   "config": {
       "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
       "database.hostname": "postgis",
       "database.port": "5432",
       "database.user": "sedona",
       "database.password": "postgis",
       "database.dbname": "sedona",
       "topic.prefix": "sedona-debezium",
       "plugin.name": "pgoutput"
   }
}'

uv run overturemaps download -f geoparquet --type=place -o sources/overture_places/places.geoparquet

docker exec -it sedona_minio mc alias set sedona http://localhost:9000 sedona sedona_password
docker exec -it sedona_minio mc mb sedona/sedona
docker exec -it sedona_minio mc cp /app/sources/ sedona/sedona/ --recursive