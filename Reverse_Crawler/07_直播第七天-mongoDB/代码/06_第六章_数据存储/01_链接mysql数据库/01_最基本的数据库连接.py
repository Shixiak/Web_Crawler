import pymysql


try:
    # 1.创建链接
    conn = pymysql.connect(
        user="root",  # The first four arguments is based on DB-API 2.0 recommendation.
        # (1045, "Access denied for user 'root'@'localhost' (using password: YES)")
        password="test123456",
        host="localhost",
        database="spider",
        port=3306,
    )

    # 目标: 执行sql语句
    # 2. 创建游标
    cursor = conn.cursor()
    # 3. 准备sql
    sql = "insert into stu_new(sname, sage, score, sgender, class) values" \
          " ('娃哈哈', 18, 66, 1, '七年五班')"

    # 4. 执行sql
    result = cursor.execute(sql)
    print(result)
    print(1/0)
    #
    # 5. 提交事务
    conn.commit()
except :
    conn.rollback()

finally:  # 最终
    if cursor:
        cursor.close()
    if conn:
        conn.close()  # 一定记得要关闭链接

# pymysql在执行sql的时候, 默认开启了事务
# 1 2 3 4 5 6 7 8 9 10
# 关于事务两个操作: rollback, commit
