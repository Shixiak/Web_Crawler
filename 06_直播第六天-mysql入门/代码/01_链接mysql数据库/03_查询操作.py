import pymysql
from pymysql.cursors import DictCursor

conn = pymysql.connect(
    user="root",  # The first four arguments is based on DB-API 2.0 recommendation.
    password="test123456",
    host="localhost",
    database="spider",
    port=3306,
)

cursor = conn.cursor(cursor=DictCursor)

sql = "select * from stu"
ret = cursor.execute(sql)

# 注意, 查询操作. 返回的数据在cursor里
# one = cursor.fetchone()  # fetchone() 一次拿出一条结果
# print(one)

# all = cursor.fetchall()  # 全拿
# print(all)

many = cursor.fetchmany(2)
print(many)

many = cursor.fetchmany(2)
print(many)

conn.close()
