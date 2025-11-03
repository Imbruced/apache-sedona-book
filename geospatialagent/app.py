import os

from fastmcp import FastMCP
from sedona.spark import SedonaContext

from src.warehouse.domain import TableInfo, Table
from src.warehouse.warehouse import SedonaWarehouse

mcp = FastMCP()

sedona = SedonaContext.builder(). \
    config("spark.sql.defaultCatalog", "sedona_catalog"). \
    getOrCreate()

warehouse = SedonaWarehouse(sedona)
warehouse.load_data()

@mcp.tool()
async def execute_query(sql: str) -> str:
    return warehouse.execute(sql)


@mcp.tool()
async def get_tables() -> list[Table]:
    return warehouse.list_tables()


@mcp.tool()
async def get_table_schema(table: str) -> TableInfo:
    return warehouse.get_table_schema(table)

@mcp.tool()
async def validate_query(sql: str) -> bool:
    return warehouse.validate_query(sql)

if __name__ == "__main__":
    host = os.getenv("MCP_HOST", "127.0.0.1")
    mcp.run(transport="http", host="0.0.0.0", port=9080)
