from airflow import DAG
import pendulum
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from chapter6.sensor import GeoParquetDataReleaseSensor

with DAG(
        dag_id="sync-overture-transportation-data",
        schedule="0 8 * * *",
        start_date=pendulum.datetime(2025, 1, 20, tz="UTC"),
        end_date=pendulum.datetime(2025, 1, 28, tz="UTC"),
        catchup=True,
        concurrency=2,
        max_active_runs=1,
        default_args={"depends_on_past": True},
):

    sensor = GeoParquetDataReleaseSensor(
        task_id="wait_for_overture_data",
        poke_interval=2,
        timeout=60 * 60 * 24,
    )

    spark_submit = SparkSubmitOperator(
        task_id="spark_submit",
        application="/opt/airflow/dags/app.py",
        conn_id="spark",
        executor_memory="2g",
        driver_memory="1g",
        executor_cores=1,
        num_executors=2,
        name="spark_job",
        verbose=True,
        conf={
            "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
            "spark.hadoop.fs.s3a.access.key": "sedona",
            "spark.hadoop.fs.s3a.secret.key": "sedona_password",
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.connection.ssl.enabled": "false",
            "spark.master": "local[*]",
        },
        application_args=["{{ ds }}"],
    )

    sensor >> spark_submit
