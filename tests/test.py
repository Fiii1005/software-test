import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse, unquote
from utils import config

def test_mysql_connection():
    database_url = urlparse(config.DATABASE_URL)
    connection = None
    try:
        connection = mysql.connector.connect(
            user=database_url.username,
            password=unquote(database_url.password),  # 解码密码
            host=database_url.hostname,
            port=database_url.port,
            database=database_url.path.lstrip('/')
        )
        if connection.is_connected():
            print("Connection successful")
            # 可以在这里添加查询操作来进一步验证数据库功能
    except Error as e:
        print("Error:", e)
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("Connection closed")

# 测试连接
test_mysql_connection()

#software-test
