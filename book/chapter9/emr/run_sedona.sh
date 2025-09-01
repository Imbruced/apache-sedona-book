#!/bin/bash

bucketName=your_sedona_application_bucket_XXXXXXXXXX  # replace with your bucket name
CLUSTER_ID=j-XXXXXXXXXXXXX  # replace with your cluster ID

aws s3 cp emr_app.py s3://${bucketName}/emr_app.py

aws emr add-steps --cluster-id ${CLUSTER_ID} \
  --steps Type=Spark,Name="Apache Sedona",ActionOnFailure=CANCEL_AND_WAIT,\
Args=[--deploy-mode,cluster,--master,yarn,s3://${bucketName}/emr_app.py]
