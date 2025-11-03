#!/bin/bash
set -e

docker-entrypoint.sh mongod &

while ! mongosh --eval 'db.adminCommand("ping")'; do
    echo "Waiting for MongoDB to be ready..."
    sleep 2
done

