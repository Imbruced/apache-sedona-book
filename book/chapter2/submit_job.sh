#!/bin/bash
docker build -t sedonaspark ./sparkcluster/spark

(cd sparkcluster; docker-compose up -d --build)

echo "Submitting Spark Job..."
docker run --network sparkcluster_default --rm \
    -v $(pwd)/sedona-initial-project/src/app.py:/opt/spark/work-dir/app.py \
    sedonaspark \
    /opt/spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    --conf spark.hadoop.fs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider \
    --conf spark.hadoop.fs.s3a.access.key=sedona \
    --conf spark.hadoop.fs.s3a.secret.key=sedona_password \
    --conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
    --conf spark.hadoop.fs.s3a.path.style.access=true \
    --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
    --conf spark.driver.extraJavaOptions="-Divy.cache.dir=/tmp -Divy.home=/tmp" \
    app.py --places_location s3a://sedona/points \
      --output_path s3a://sedona/output