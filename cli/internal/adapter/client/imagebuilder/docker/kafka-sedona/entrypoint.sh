#!/bin/bash
set -e

/__cacert_entrypoint.sh /etc/kafka/docker/run &

while ! /opt/kafka/bin/kafka-broker-api-versions.sh --bootstrap-server localhost:9092; do
    echo "Waiting for Kafka to be ready..."
    sleep 2
done

echo "✅ Kafka is ready."
sleep infinity