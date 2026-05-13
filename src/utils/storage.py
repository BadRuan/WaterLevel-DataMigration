from typing import List, Any, Optional
from itertools import batched
from asyncpg import connect
from settings import postgres
from model import Station


class Storage():   
    def __init__(self) -> None:
        self.connection = None
        self.initialized = None
    
    async def __aenter__(self):
        await self.ensure_initialized()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection is not None:
            await self.connection.close()
    
    async def ensure_initialized(self):
        if self.initialized is None:
            await self.init_connect()
            
    async def init_connect(self):
        self.connection = await connect(host=postgres.url, user=postgres.user, password=postgres.password, port=postgres.port, database=postgres.database)
                   
    async def query_one(self, sql: str) -> Optional[Any]:
        if self.connection is not None:
            result = await self.connection.fetchrow(sql)
            if result is None:
                return None
            else:
                return result
        else:
            return ''
        
    async def query_list(self, sql: str) -> List[Any]:
        if self.connection is not None:
            return await self.connection.fetch(sql)
        else:
            return []
    
    async def save(self, sql: str) -> int:
        if self.connection is not None:
            affected_rows:int = await self.connection.execute(sql)
            return affected_rows
        else:
            return 0
    
    async def insert_waterlevel(self, station: Station):
        """保存水位数据

        Args:
            station (Station): 站点模型
        """       
        SQL = f"""INSERT INTO station_{station.code} (ts, height) VALUES """
        if len(station.water_items) > 0:
           for wateritem_list in batched(station.water_items, n=1000):
                sql = SQL
                for water_item in wateritem_list:
                    sql += f"('{water_item.timestamp}', {water_item.height}),"
                sql= sql[:-1] + "ON CONFLICT (ts) DO NOTHING;"
                await self.save(sql)