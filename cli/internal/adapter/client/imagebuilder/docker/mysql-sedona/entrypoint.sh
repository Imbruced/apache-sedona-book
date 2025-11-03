#!/bin/bash
set -e

docker-entrypoint.sh mysqld &

while ! mysqladmin ping -h localhost -u root --silent; do
    echo "Waiting for MySQL to be ready..."
    sleep 2
done

/app/migrate.sh || true

echo "✅ MySQL migration completed."
sleep infinity