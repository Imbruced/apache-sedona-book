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