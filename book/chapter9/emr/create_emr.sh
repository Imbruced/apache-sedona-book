#!/bin/bash

SEDONA_VERSION=1.7.2
SPARK_VERSION=3.5
SCALA_VERSION=2.12
GEOTOOLS_VERSION=28.5
SUBNET_ID="YOUR_SUBNET_ID"

# create s3 bucket to store jar files
bucketName=your_sedona_bucket_$(date +%s)

aws s3 mb s3://${bucketName}

# upload initialization script to the S3 bucket
aws s3 cp init.sh s3://${bucketName}/init.sh

# sed configuration script
config=$(sed -e "s|<SPARK_VERSION>|$SPARK_VERSION|g" -e "s|<SCALA_VERSION>|$SCALA_VERSION|g" -e "s|<SEDONA_VERSION>|$SEDONA_VERSION|g" -e "s|<GEOTOOLS_VERSION>|$GEOTOOLS_VERSION|g" configurations.json)

# create default roles
aws emr create-default-roles

# create EMR cluster
aws emr create-cluster \
    --release-label emr-7.8.0 \
    --instance-type m1.large \
    --use-default-roles \
    --applications Name=Spark \
    --instance-count 1 \
    --bootstrap-actions Path=s3://${bucketName}/init.sh,Name=InitializeSedona,Args=[] \
    --configurations "${config}" \
    --ec2-attributes SubnetId=${SUBNET_ID} \
    --log-uri s3://${bucketName}/logs/

#change to --ec2-attributes SubnetId=${SUBNET_ID},KeyName=sedona-key-pair if you need to ssh to the machine
