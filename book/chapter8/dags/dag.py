import os.path

from airflow import DAG
import pendulum
from airflow.providers.apache.spark.operators.spark_sql import SparkSqlOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.decorators import task_group


CONN_ID = "spark"
SQL_PATH = "/opt/airflow/dags/sql"
APP_PATH = "/opt/airflow/dags/apps"
CATALOG_NAME = "sedona_catalog"
STG_DATABASE = "stg_risk_management"
PROD_DATABASE = "risk_management"


def get_sql_from_file(file_name: str) -> str:
    with open(f"dags/sql/{file_name}") as file:
        return file.read()


def create_sql_operator_from_file(sql_file_name: str, **kwargs) -> SparkSqlOperator:
    return SparkSqlOperator(
        conn_id=CONN_ID,
        task_id=kwargs.get("task_id", sql_file_name.replace(".sql", "")),
        sql=get_sql_from_file(sql_file_name).format(**kwargs)
    )


def load_sql(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def create_spark_submit_operator(script: str, arguments: list[str]) -> SparkSubmitOperator:
    return SparkSubmitOperator(
        conn_id=CONN_ID,
        task_id=script.replace(".py", ""),
        application=os.path.join(APP_PATH, script),
        application_args=arguments,
        executor_memory="5G",
        driver_memory="5G",
        num_executors=12,
    )

def create_task_group(
        task_group_id: str,
        script_file_name: str,
        arguments: list[str],
):
    @task_group(group_id=task_group_id)
    def run_test_group():
        run_operator = create_spark_submit_operator(
            script_file_name,
            arguments,
        )

        run_test_operator = create_spark_submit_operator(
            script_file_name.replace(".py", "_test.py"),
            arguments
        )

        run_operator >> run_test_operator

    return run_test_group




with DAG(
        dag_id="geospatial-lakehouse",
        schedule="0 15 * * *",
        start_date=pendulum.datetime(2025, 1, 10, tz="UTC"),
        catchup=False,
        tags=["example"],
        concurrency=2,
        max_active_runs=1,
) as test_run_dag:
    # DDLS
    create_catalog = create_sql_operator_from_file(
        sql_file_name="create_catalog.sql",
        catalog=CATALOG_NAME,
        database=STG_DATABASE,
    )

    create_catalog_prod = create_sql_operator_from_file(
        sql_file_name="create_catalog.sql",
        task_id="create_catalog_prod",
        catalog=CATALOG_NAME,
        database=PROD_DATABASE,
    )

    netherlands_shape = create_sql_operator_from_file(
        sql_file_name="nl_shape_ddl.sql",
        catalog=CATALOG_NAME,
        database=STG_DATABASE,
    )

    buildings_table = create_sql_operator_from_file(
        sql_file_name="nl_buildings_ddl.sql",
        catalog=CATALOG_NAME,
        database=STG_DATABASE,
    )

    flood_table = create_sql_operator_from_file(
        sql_file_name="nl_flood_ddl.sql",
        catalog=CATALOG_NAME,
        database=STG_DATABASE,
    )

    nl_road_risk_score_table = create_sql_operator_from_file(
        sql_file_name="nl_road_risk_score_ddl.sql",
        catalog=CATALOG_NAME,
        database=STG_DATABASE,
    )

    nl_transportation_table = create_sql_operator_from_file(
        sql_file_name="nl_transportation_ddl.sql",
        catalog=CATALOG_NAME,
        database=STG_DATABASE,
    )

    nl_transportation_hex_bins_table = create_sql_operator_from_file(
        sql_file_name="nl_transportation_hex_bins_ddl.sql",
        catalog=CATALOG_NAME,
        database=STG_DATABASE,
    )

    risk_score_task_group = create_task_group(
        "nl_risk_score",
        "nl_risk_score.py",
        ["{{ ds }}", STG_DATABASE, STG_DATABASE],
    )
    #
    netherlands_flood_raster = create_spark_submit_operator(
        "nl_flood_map.py",
        ["{{ ds }}", STG_DATABASE, STG_DATABASE],
    )

    netherlands_transportation = create_spark_submit_operator(
        "nl_transportation.py",
        ["{{ ds }}", STG_DATABASE, STG_DATABASE],
    )

    netherlands_transportation_hex_bins = create_spark_submit_operator(
        "nl_hex_grids.py",
        ["{{ ds }}", STG_DATABASE, STG_DATABASE],
    )

    risk_score_task_group_task = risk_score_task_group()

    nl_shape = create_spark_submit_operator(
        "nl_shape.py", ["{{ ds }}", STG_DATABASE, STG_DATABASE]
    )

    building_task_group = create_task_group(
        "building_task_group",
        "nl_buildings.py",
        ["{{ ds }}", STG_DATABASE, STG_DATABASE],
    )

    building_task_group_task = building_task_group()

    ddls = [
        netherlands_shape,
        buildings_table,
        flood_table,
        nl_road_risk_score_table,
        nl_transportation_table,
        nl_transportation_hex_bins_table
    ]

    create_catalog >> ddls
    nl_shape << ddls
    [nl_shape, buildings_table] >> building_task_group_task
    [netherlands_shape, flood_table] >> netherlands_flood_raster
    [netherlands_shape, nl_transportation_table] >> netherlands_transportation

    [netherlands_transportation, nl_transportation_hex_bins_table] >> netherlands_transportation_hex_bins

    [
        nl_road_risk_score_table,
        building_task_group_task,
        netherlands_flood_raster,
        netherlands_transportation_hex_bins,
    ] >> risk_score_task_group_task


    # PROD
    netherlands_risk_score_prod = create_spark_submit_operator(
        "nl_road_risk_score_prod.py",
        ["{{ ds }}", STG_DATABASE, PROD_DATABASE],
    )

    netherlands_risk_score_table_prod = create_sql_operator_from_file(
        sql_file_name="nl_road_risk_score_ddl.sql",
        catalog=CATALOG_NAME,
        database=PROD_DATABASE,
        task_id="nl_road_risk_score_ddl_prod",
    )

    [create_catalog_prod, risk_score_task_group_task, netherlands_risk_score_table_prod] >> netherlands_risk_score_prod

