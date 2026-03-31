# 水位数据迁移

## 1、概述

本项目主要是为解决水位数据库迁移而写，最初想写的是从TDengine直接将数据迁移至PostgreSQL，后来发现TDengine数据库官方文档描述和官方代码库不相符，直接迁移数据走不通。
遂决定将相关数据转成csv文件，再从csv文件写入到PostgreSQL，本项目实际为此思路的具体实现。

## 2、技术栈

1. Python
2. PostgreSQL

## 3、部分过程记录

原本想一条一条读取并验证目标数据库是否已有数据，若有不写入，后来发现PostgreSQL的SQL语言本身就有冲突不录入的机制，真的省心省事。再说一条条写入，变成一次性写入1000条sql语句，效率提了上来，总共100多万条数据，没一会就能按照计划迁移成功。

## 4、相关sql备份

### TDengine 数据

表名：`t站点代码`

列名：

- `current` : `float` 当前水位
- `ts` : `timestamp` 具体时间

数据表：

1. `t60115400`： 芜湖
2. `t62904400`： 凤凰颈闸下
3. `t62900700`： 裕溪闸下
4. `t62900600`： 裕溪闸上
5. `t62906500`： 清水
6. `t62905100`： 新桥闸上

### PostgreSQL 数据

表名：`station_站点代码`

列名：

- `ts`：`TIMESTAMP` 具体时间，不带时区
- `height`：`numeric(5, 2)` 水位高程

```sql
-- 创建基础表
create table if not exists station (
 ts timestamp primary key unique not null,
 height numeric(5, 2) not null
);

-- 使用PostgreSQL表继承特性
create table if not exists station_60115400 (
 like station including all
) inherits (station);
create table if not exists station_62904400 (
 like station including all
) inherits (station);
create table if not exists station_62900700 (
 like station including all
) inherits (station);
create table if not exists station_62900600 (
 like station including all
) inherits (station);
create table if not exists station_62906500 (
 like station including all
) inherits (station);
create table if not exists station_62905100 (
 like station including all
) inherits (station);

-- 插入水位数据
insert into station_60115400 (ts, height)
values
('2026-03-24 13:23:00', 12.3),
('2026-03-24 13:20:00', -2.3)
ON CONFLICT (ts) 
DO NOTHING;

insert into station_62904400 (ts, height)
values
('2026-03-24 13:23:00', 12.3),
('2026-03-24 13:20:00', -2.3)
ON CONFLICT (ts) 
DO NOTHING;
```
