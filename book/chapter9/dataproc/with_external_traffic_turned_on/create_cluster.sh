BUCKET_NAME=YOUR_BUCKET

gcloud dataproc clusters create apache-sedona-cluster \
  --enable-component-gateway --region europe-west1 \
  --no-address --master-machine-type n2-standard-2 \
  --master-boot-disk-type pd-balanced --master-boot-disk-size 30 \
  --num-workers 2 --worker-machine-type n2-standard-2 \
  --worker-boot-disk-type pd-balanced --worker-boot-disk-size 30 \
  --project solar-grail-453220-n9 \
  --image-version 2.2-ubuntu22 \
  --initialization-actions gs://${BUCKET_NAME}/init.sh