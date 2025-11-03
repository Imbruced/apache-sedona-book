#!/bin/bash
set -e

tini -- /docker-entrypoint.sh &

until curl --silent --fail http://localhost:5678/healthz; do
  echo "Waiting for n8n to be ready..."
  sleep 2
done

n8n import:workflow --input workflow.json

echo "✅ n8n is ready!"
sleep infinity