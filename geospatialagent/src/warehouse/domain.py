from dataclasses import dataclass


@dataclass
class Table:
    name: str


@dataclass
class TableInfo:
    name: str
    schema: dict[str, str]
