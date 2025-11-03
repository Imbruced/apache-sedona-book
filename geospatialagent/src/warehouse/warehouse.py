import json
import sys
from io import StringIO

from pyspark.sql.connect.session import SparkSession

from src.warehouse.domain import Table, TableInfo


class SedonaWarehouse:
    def __init__(self, sedona: SparkSession):
        self.sedona = sedona

    def load_data(self):
        self.sedona.read.format("geoparquet").\
            load("s3a://apache-sedona-book/source_data/warehouse/buildings/").\
            createOrReplaceTempView("buildings")

        self.sedona.read.format("geoparquet").\
            load("s3a://apache-sedona-book/source_data/warehouse/places/").\
            createOrReplaceTempView("places")

    def execute(self, sql: str) -> str:
        result_df = self.sedona.sql(sql)

        buffer = StringIO()
        old_stdout = sys.stdout
        sys.stdout = buffer

        result_df.show()

        sys.stdout = old_stdout
        df_string = buffer.getvalue()

        return df_string


    def get_table_schema(self, table_name: str) -> TableInfo:
        return TableInfo(
            name=table_name,
            schema=json.loads(self.sedona.table(table_name).schema.json()),
        )

    def list_tables(self) -> list[Table]:
        self.sedona.sql("show tables").show()

        tables = self.sedona.sql("show tables"). \
            selectExpr("tableName AS name"). \
            collect()

        return [
            Table(
                name=row["name"],
            )
            for row in tables
        ]

    def validate_query(self, sql: str) -> bool:
        try:
            self.sedona.sql(sql).explain()
            return True
        except Exception:
            return False
