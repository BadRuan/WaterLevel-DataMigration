from typing import List
from psycopg2 import connect as pq_connect
from model import WaterItem, Station
from config import postgres


class PostgresStorage():   
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None
        self.initialized = None
    
    async def __aenter__(self):
        await self.ensure_initialized()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()
   
    
    async def ensure_initialized(self):
        if self.initialized is None:
            self.init_connect()
            
    async def execute(self) -> None:
        await self.ensure_initialized()


    def init_connect(self):
        self.connection = pq_connect(host=postgres.url, user=postgres.user, password=postgres.password, port=postgres.port, database=postgres.database)
        if self.connection is not None:    
            self.cursor = self.connection.cursor()
              
    async def save(self, sql: str) -> None:
        await self.execute()
        if self.cursor is not None and self.connection is not None:
            self.cursor.execute(sql)
            self.connection.commit()
        
    async def query(self, sql: str) -> List:
        await self.execute()
        if self.cursor is not None:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        else:
            return []
    
    async def insert_waterlevel(self, station: Station):
        # 防止数据过多拼接sql语句过长，对数据进行切片处理
        def slice_list(data: List, length: int = 1000):
            return [data[i : i + length] for i in range(0, len(data), length)]

        SQL = f"""INSERT INTO station_{station.code} (ts, height)
                VALUES"""

        if len(station.water_items) > 0:

            slice_data: List[WaterItem] = slice_list(station.water_items) # type: ignore
            
            for wateritem_list in slice_data:
                sql = SQL
                for water_item in wateritem_list: # type: ignore
                    sql += f"('{water_item.timestamp}', {water_item.height}),"
                sql= sql[:-1] + "ON CONFLICT (ts) DO NOTHING;"
                await self.save(sql + ";")