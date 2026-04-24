from typing import NamedTuple, List, Tuple, Generator
from model import Station


class DataConfig(NamedTuple):
    url: str
    user: str
    password: str
    port: int
    database: str

type station_item = Tuple[int, str]

postgres = DataConfig(url='100.68.9.83', user='postgres', password='Deepseek666', port=54321, database='water') 

file_path: str = './data/waterlevel_202601141954.csv'

Stations: List[station_item] = [
    (60115400, "芜湖"),
    (62904500, "凤凰颈闸下"),
    (62900700, "裕溪闸下"),
    (62900600, "裕溪闸上"),
    (62906500, "清水"),
    (62905100, "新桥闸上"),
]

stations_list: List[Station] = [Station(name=station[1], code=station[0], water_items=[]) for station in Stations]
