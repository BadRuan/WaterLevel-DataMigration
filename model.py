from dataclasses import dataclass
from typing import List 


@dataclass
class WaterItem:
    timestamp: str
    height: float

@dataclass
class Station:
    name: str
    code: int
    water_items: List[WaterItem]
    

Stations: List[Station] = [
    Station(code=60115400, name="芜湖", water_items=[]),
    Station(code=62904500, name="凤凰颈闸下", water_items=[]),
    Station(code=62900700, name="裕溪闸下", water_items=[]),
    Station(code=62900600, name="裕溪闸上", water_items=[]),
    Station(code=62906500, name="清水", water_items=[]),
    Station(code=62905100, name="新桥闸上", water_items=[]),
]