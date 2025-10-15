#!/bin/bash

prefect server start --host 0.0.0.0 &
echo "Prefect server started"

prefect block register -f block.py
prefect work-pool create sedona-pool --type process
prefect deploy

# wait for the server to be fully up and running
export PREFECT_API_URL=http://localhost:4200/api
prefect worker start --pool sedona-pool &

prefect --no-prompt deploy

sleep 1000