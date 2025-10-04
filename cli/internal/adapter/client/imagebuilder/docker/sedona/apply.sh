#!/usr/bin/env bash

/opt/start.sh &
PID=$!

sleep 5
if [[ "$SEDONA_COPY_MINIO" = "true" ]]; then
  echo "Copying data from MinIO to local storage..."
    cp s3-conf.conf /opt/spark/conf/spark-defaults.conf
    sed -i -e "s|<AWS_ACCESS_KEY_ID>|$AWS_ACCESS_KEY_ID|g" -e "s|<AWS_SECRET_ACCESS_KEY>|$AWS_SECRET_ACCESS_KEY|g" /opt/spark/conf/spark-defaults.conf
else
  cp s3-conf.conf /opt/spark/conf/spark-defaults.conf
  sed -i -e "s|<AWS_ACCESS_KEY_ID>|$AWS_ACCESS_KEY_ID|g" -e "s|<AWS_SECRET_ACCESS_KEY>|$AWS_SECRET_ACCESS_KEY|g" /opt/spark/conf/spark-defaults.conf
fi

wait $PID
