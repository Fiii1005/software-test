import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse, unquote
import pandas as pd
import os
from utils import config

# 数据库连接
def create_connection():
    database_url=urlparse(config.DATABASE_URL);
    try:
        connection = mysql.connector.connect(
            user='root',
            password=config.PASSWORD,  # 解码密码
            host='localhost',
            port='3306',
            database=config.DATABASE
        )
        if connection.is_connected():
            print("Connection successful")
            return connection
    except Error as e:
        print("Error:", e)
        return None

# 关闭数据库连接
def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print("Connection closed")

# 创建水体物理数据表
def create_water_physic_table(connection):
    # 创建执行数据库查询的上下文游标
    cursor = connection.cursor()
    # 定义创建表的 SQL 语句
    create_table_query = """
    CREATE TABLE IF NOT EXISTS water_physic (
        station_id VARCHAR(255) NOT NULL,
        time DATE NOT NULL,
        depth DOUBLE,
        temperature DOUBLE,
        transparency DOUBLE,
        solids DOUBLE,
        electrical_conductivity INT,
        PRIMARY KEY (station_id, time)
    )
    """
    # 执行创建表的操作
    cursor.execute(create_table_query)
    # 提交事务
    connection.commit()
    # 关闭游标
    cursor.close()
    print("Water physic table created successfully")


# 上传水质物理数据
def upload_water_physic(connection):
    # 获取当前脚本文件的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建数据集文件的绝对路径
    WP_data_file_path = os.path.join(current_dir, 'dataset', '2001-2006Physics.csv')
    # 读取 CSV 文件
    data = pd.read_csv(WP_data_file_path, delimiter=',', header=0, names=['站点', '年', '月', '水深/m', '水温/℃', '透明度/m', '悬浮质/mg/L', '电导率/µS/cm'])
    # 填充空值为0
    data.fillna(0, inplace=True)
    # 创建执行数据库查询的上下文游标
    cursor = connection.cursor()
    # 定义了SQL插入语句
    insert_query = """
    INSERT INTO water_physic (station_id, time, depth, temperature, transparency, solids, electrical_conductivity)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    for index, row in data.iterrows():
        year = int(row['年'])
        month = int(row['月'])
        date = f"{year}-{month:02d}-01"
        values = (row['站点'], date, row['水深/m'], row['水温/℃'], row['透明度/m'], row['悬浮质/mg/L'], row['电导率/µS/cm'])
        cursor.execute(insert_query, values)
    connection.commit()
    cursor.close()
    print("Data uploaded successfully")

# 创建水质化学数据表
def create_water_chemistry_table(connection):
    # 创建执行数据库查询的上下文游标
    cursor = connection.cursor()
    # 定义创建表的 SQL 语句
    create_table_query = """
    CREATE TABLE IF NOT EXISTS water_chemistry (
        station_id VARCHAR(255) NOT NULL,
        time DATE NOT NULL,
        pH DOUBLE,
        total_N DOUBLE,
        total_P DOUBLE,
        chlorophyll DOUBLE,
        chl_without_Mg DOUBLE,
        kmno4 DOUBLE,
        dissolved_o DOUBLE,
        BOD5 DOUBLE,
        NH4N DOUBLE,
        HNO2 DOUBLE,
        NO3 DOUBLE,
        dissolved_N DOUBLE,
        phosphate DOUBLE,
        dissolved_P DOUBLE,
        alkalinity DOUBLE,
        potassium_lon DOUBLE,
        sodium_lon DOUBLE,
        calcium_lon DOUBLE,
        magnesium_lon DOUBLE,
        fluoride_lon DOUBLE,
        chloride DOUBLE,
        sulfate DOUBLE,
        silicate DOUBLE,
        alkalinity_as_caco3 DOUBLE,
        silicate_as_si DOUBLE,
        PRIMARY KEY (station_id, time)
    )
    """
    # 执行创建表的操作
    cursor.execute(create_table_query)
    # 提交事务
    connection.commit()
    # 关闭游标
    cursor.close()
    print("Water chemistry table created successfully")

# 上传水质化学数据
def upload_water_chemistry(connection):
    # 获取当前脚本文件的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建数据集文件的绝对路径
    WC_data_file_path = os.path.join(current_dir, 'dataset', '2001-2006Chemistry.csv')
    # 读取 CSV 文件
    data = pd.read_csv(WC_data_file_path)
    # 填充空值为0
    data.fillna(0, inplace=True)
    # 创建执行数据库查询的上下文游标
    cursor = connection.cursor()
    # 定义SQL插入语句
    insert_query = """
    INSERT INTO water_chemistry (
    station_id, time, pH, total_N, total_P, chlorophyll, chl_without_Mg,
    kmno4, dissolved_o, BOD5, NH4N, HNO2, NO3, dissolved_N, phosphate,
    dissolved_P, alkalinity, potassium_lon, sodium_lon, calcium_lon,
    magnesium_lon, fluoride_lon, chloride, sulfate, silicate,
    alkalinity_as_caco3, silicate_as_si) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for index, row in data.iterrows():
        # 构建数据元组
        values = (
            row['站点'], f"{row['年']}-{row['月']:02d}-01", row['pH'], row['总氮(mg/L)'],
            row['总磷(mg/L)'], row['叶绿素a(μg/L)'], row['脱镁叶绿素(μg/L)'],
            row['高锰酸盐指数(mg/L)'], row['溶解氧(mg/L)'], row['五日生化需氧量(mg/L)'],
            row['氨氮(mg/L)'], row['亚硝酸盐氮(mg/L)'], row['硝酸盐氮(mg/L)'],
            row['溶解性总氮(mg/L)'], row['磷酸盐(mg/L)'], row['溶解性总磷(mg/L)'],
            row['碱度(mmol/L)'], row['钾离子(mg/L)'], row['钠离子(mg/L)'],
            row['钙离子(mg/L)'], row['镁离子(mg/L)'], row['氟离子(mg/L)'],
            row['氯化物(mg/L)'], row['硫酸盐(mg/L)'], row['硅酸盐(µmol/L)'],
            row['碱度（CaCO3 计）(mg/L)'], row['硅酸盐（mg/L）']
        )
        # 执行插入操作
        cursor.execute(insert_query, values)
    # 提交事务
    connection.commit()
    # 关闭游标
    cursor.close()
    print("Water chemistry data uploaded successfully")

# 创建鱼类数据库
def create_fish_table(connection):
    # 创建执行数据库查询的上下文游标
    cursor = connection.cursor()
    # 定义创建表的 SQL 语句
    create_table_query = """
    CREATE TABLE IF NOT EXISTS fish_2 (
        date DATE NOT NULL,
        fishname VARCHAR(255) NOT NULL,
        lengthrange VARCHAR(255) NOT NULL,
        weightrange VARCHAR(255) NOT NULL,
        num INT,
        PRIMARY KEY (date, fishname, lengthrange, weightrange)
    )
    """
    # 执行创建表的操作
    cursor.execute(create_table_query)
    # 提交事务
    connection.commit()
    # 关闭游标
    cursor.close()
    print("Fish table created successfully")

# 上传鱼类数据
def upload_fish(connection):
    # 获取当前脚本文件的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建数据集文件的绝对路径
    WC_data_file_path = os.path.join(current_dir, 'dataset', 'fish.csv')
    # 读取 CSV 文件
    data = pd.read_csv(WC_data_file_path)
    # 填充空值为0
    data.fillna(0, inplace=True)
    # 创建执行数据库查询的上下文游标
    cursor = connection.cursor()
    # 定义SQL插入语句
    insert_query = """
    INSERT INTO fish_2 (
    date, fishname, lengthrange, weightrange, num) VALUES (
    %s, %s, %s, %s, %s)
    """
    for index, row in data.iterrows():
        # 构建数据元组
        values = (
            f"{row['年']}-{row['月']:02d}-{row['日']:02d}", row['鱼'], row['范围（长度cm）'],
            row['范围（重量kg）'], row['数量']
        )
        # 执行插入操作
        cursor.execute(insert_query, values)
    # 提交事务
    connection.commit()
    # 关闭游标
    cursor.close()
    print("fish data uploaded successfully")

def create_user_table(connection):
    # 创建执行数据库查询的上下文游标
    cursor = connection.cursor()

    # 定义创建表的 SQL 语句
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        name VARCHAR(255),
        gender VARCHAR(255),
        age INT,
        phone_number VARCHAR(255),
        email VARCHAR(255),
        role VARCHAR(255)
    )
    """

    # 执行创建表的操作
    cursor.execute(create_table_query)
    
    # 提交事务
    connection.commit()
    
    # 关闭游标
    cursor.close()
    
    print("User table created successfully")

# 创建数据库连接
connection = create_connection()

# 创建水质物理数据表
#create_water_physic_table(connection)

# 上传水质物理数据到数据库
#upload_water_physic(connection)

# 创建水质化学数据表
#create_water_chemistry_table(connection)

# 上传水质化学数据到数据库
#upload_water_chemistry(connection)

# 创建鱼类数据表
create_fish_table(connection)

# 上传鱼类数据
upload_fish(connection)

# 创建用户表
#create_user_table(connection)

# 关闭数据库连接
close_connection(connection)