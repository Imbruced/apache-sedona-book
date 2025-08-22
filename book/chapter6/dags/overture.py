from airflow import DAG
import pendulum
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from sensor import GeoParquetDataReleaseSensor

packages = [
    # 'org.apache.hadoop:hadoop-aws:3.3.4',
    # 'org.apache.hadoop:hadoop-client-api:3.3.4',
    # 'org.apache.hadoop:hadoop-common:3.3.4',
    # 'org.apache.sedona:sedona-spark-3.5_2.12:1.7.0',
    # 'org.datasyslab:geotools-wrapper:1.7.0-28.5',
    # 'uk.co.gresearch.spark:spark-extension_2.12:2.11.0-3.4',
]

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
        # packages=",".join(packages),
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
