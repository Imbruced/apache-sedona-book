#!/bin/bash
set -e

/docker-entrypoint.sh start &

while ! curl -s http://localhost:8083/; do
    echo "Waiting for Debezium to be ready..."
    sleep 2
done

./create-connector.sh

echo "✅ Debezium connector creation completed."