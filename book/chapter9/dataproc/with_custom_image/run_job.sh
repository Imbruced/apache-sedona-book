gcloud dataproc jobs submit pyspark \
    gs://ptokaj-bucket-sedona/application.py \
    --cluster=apache-sedona-cluster \
    --region=europe-west1