#!/bin/bash
docker build -t sedonaspark ./sparkcluster/spark

docker run --network sparkcluster_default --rm \
    -v $(pwd)/sedona-initial-project/src/app.py:/opt/spark/work-dir/app.py \
    sedonaspark \
    /opt/spark/bin/spark-submit \
    --packages org.apache.sedona:sedona-spark-3.5_2.12:1.7.0,org.datasyslab:geotools-wrapper:1.7.0-28.5,org.apache.hadoop:hadoop-aws:3.3.4,org.apache.hadoop:hadoop-client-api:3.3.4,org.apache.hadoop:hadoop-common:3.3.4 \
    --master spark://spark-master:7077 \
    --conf spark.hadoop.fs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider \
    --conf spark.hadoop.fs.s3a.access.key=sedona \
    --conf spark.hadoop.fs.s3a.secret.key=sedona_password \
    --conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
    --conf spark.hadoop.fs.s3a.path.style.access=true \
    --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
    --conf spark.driver.extraJavaOptions="-Divy.cache.dir=/tmp -Divy.home=/tmp" \
    app.py --places_location s3a://sedona/points \
      --output_path s3a://sedona/output \
      --env prod
