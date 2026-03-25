from dataclasses import dataclass


@dataclass
class WaterItem:
    timestamp: str
    height: float
    code: int
    name: str
    table_name: str
    