from typing import NamedTuple


class DataConfig(NamedTuple):
    url: str
    user: str
    password: str
    port: int
    database: str
    
postgres = DataConfig(url='100.95.218.64', user='postgres', password='E,*f*YdGgYSgqfze1tLqc0Pm8CK2', port=44455, database='water') 


file_path: str = '.data/waterlevel_202601141954.csv'
