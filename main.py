from pandas import read_csv
from storage import console
from handle import WaterItem
from storage import PostgresStorage
from rich.progress import Progress
from asyncio import run


async def main():
    console.print('run start')

    file_path: str = "waterlevel_202601141954.csv"

    df = read_csv(file_path, header=0)
    total_count: int = len(df)   
    with Progress() as progress:
        task = progress.add_task("数据迁移中", total=total_count)
        async with PostgresStorage() as storage:
            for index, row in df.iterrows():
                date_item = row.tolist()
                w = WaterItem(
                    timestamp=date_item[0],
                    height=float(date_item[1]),
                    code=int(date_item[2]),
                    name=date_item[3],
                    table_name=date_item[4]
                    )
                insert_sql: str = f"insert into station_{w.code} (ts, height) values ('{w.timestamp}', {w.height});"
                query_sql: str = f"select (ts, height) from station_{w.code} where ts='{w.timestamp}';"
                
                result_count: int = len(await storage.query(query_sql))
                if 0 == result_count:
                    await storage.save(insert_sql)
                    progress.console.log(f"新增{w.name}站 {w.timestamp[:-4]} {w.height} m数据")
                else:
                    progress.console.log(f"已有数据: {w.name}站 {w.timestamp[:-4]} {w.height} m数据")
                
            
    
    console.print('run end')


if __name__ == "__main__":
    run(main())
