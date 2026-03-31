from pandas import read_csv
from rich.console import Console
from model import WaterItem, Stations
from storage import PostgresStorage
from asyncio import run 

console = Console()
log = console.print

async def main():
    try:
        file_path: str = 'waterlevel_202601141954.csv'
        df = read_csv(file_path, header=0)
        total_count: int = len(df)
        log(f"csv文件中总共有 {total_count} 条水位数据")
        flag:int = 0
        for index, row in df.iterrows():
            flag = index # type: ignore
            date_item = row.tolist()
            w = WaterItem(timestamp=date_item[0], height=float(date_item[1]))
            code: int = int(date_item[2])
            for station in Stations:
                if code == station.code:
                    station.water_items.append(w)
        for station in Stations:
            async with PostgresStorage() as storage: # type: ignore
                await storage.insert_waterlevel(station)
                log(f"{station.name}站有 {len(station.water_items)} 条水位数据")
    except ValueError as e:
        log(e)
    finally:
        log(f"index: {flag}")

if __name__ == "__main__":
    run(main())