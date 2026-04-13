from typing import NamedTuple, List, Tuple
from model import Station


class DataConfig(NamedTuple):
    url: str
    user: str
    password: str
    port: int
    database: str
    
postgres = DataConfig(url='100.95.218.64', user='postgres', password='E,*f*YdGgYSgqfze1tLqc0Pm8CK2', port=44455, database='water') 

file_path: str = '../data/waterlevel_202601141954.csv'

Stations: List[Tuple[int, str]] = [
    (60115400, "芜湖"),
    (62904500, "凤凰颈闸下"),
    (62900700, "裕溪闸下"),
    (62900600, "裕溪闸上"),
    (62906500, "清水"),
    (62905100, "新桥闸上"),
]

stations_list: List[Station] = [Station(name=s[1], code=s[0], water_items=[]) for s in Stations]
