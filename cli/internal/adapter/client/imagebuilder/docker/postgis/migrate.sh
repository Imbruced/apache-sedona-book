psql -h localhost -U postgis -d postgis -f /app/postgis.sql
psql -h localhost -U sedona -d sedona -f /app/postgis_ddl.sql
