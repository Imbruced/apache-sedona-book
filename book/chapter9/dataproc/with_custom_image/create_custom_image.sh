#!/bin/bash
set -e

PROJECT_ID="YOUR_PROJECT_ID"
YOUR_CUSTOM_IMAGE_NAME="apache-sedona"

python3 generate_custom_image.py \
    --image-name=${YOUR_CUSTOM_IMAGE_NAME} \
    --dataproc-version=2.2-ubuntu22 \
    --customization-script=init.sh \
    --zone=europe-west1-b \
    --gcs-bucket=you_bucket


# create cluster
gcloud dataproc clusters create apache-sedona-cluster \
  --enable-component-gateway --region europe-west1 \
  --no-address --master-machine-type n2-standard-2 \
  --master-boot-disk-type pd-balanced --master-boot-disk-size 40 \
  --num-workers 2 --worker-machine-type n2-standard-2 \
  --worker-boot-disk-type pd-balanced --worker-boot-disk-size 40 \
  --project ${PROJECT_ID} \
  --image https://www.googleapis.com/compute/v1/projects/${PROJECT_ID}/global/images/${YOUR_CUSTOM_IMAGE_NAME}