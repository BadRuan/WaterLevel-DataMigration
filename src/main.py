from asyncio import run
from pandas import read_csv
from utils import Storage, log
from model import WaterItem
from settings import file_path, stations_list


async def main():
    try:
        df = read_csv(file_path, header=0)
        total_count: int = len(df)
        log(f"csv文件中总共有 {total_count} 条水位数据")
        for index, row in df.iterrows():
            date_item = row.tolist()
            w = WaterItem(timestamp=date_item[0], height=float(date_item[1]))
            code: int = int(date_item[2])
            for station in stations_list:
                if code == station.code:
                    station.water_items.append(w)
        for station in stations_list:
            async with Storage() as storage:
                await storage.insert_waterlevel(station)
                log(f"{station.name}站有 {len(station.water_items)} 条水位数据")
    except ValueError as e:
        log(e)
    finally:
        log('End')


if __name__ == "__main__":
    run(main())
