from typing import NamedTuple, List


class WaterItem(NamedTuple):
    timestamp: str
    height: float

class Station(NamedTuple):
    name: str
    code: int
    water_items: List[WaterItem]
    