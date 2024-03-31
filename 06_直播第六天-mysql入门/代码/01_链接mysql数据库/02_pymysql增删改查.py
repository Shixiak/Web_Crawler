import pymysql
from pymysql.cursors import DictCursor

# 通过函数对pymysql进行极简单的封装


def get_conn():
    conn = pymysql.connect(
        user="root",
        password="test123456",
        host="localhost",
        database="spider",
        port=3306,
    )
    return conn


def change(sql, isInsert=False):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        count = cursor.execute(sql)
        conn.commit()
        if isInsert:
            # 新增的数据的id值
            new_id = cursor.lastrowid
            return new_id
        else:
            return count
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def add(sql):
    return change(sql, isInsert=True)


def upd(sql):
    return change(sql)


def delete(sql):
    return change(sql)


def get_one(sql):
    try:
        conn = get_conn()
        cursor = conn.cursor(cursor=DictCursor)
        cursor.execute(sql)
        return cursor.fetchone()
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_all(sql):
    try:
        conn = get_conn()
        cursor = conn.cursor(cursor=DictCursor)
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    # sql = "insert into stu_new(sname, sgender, sage, score, class) values ('完蛋了', 1, 18, 88, '五年六班')"
    # ret = add(sql)
    # print(ret)

    # sql = "update stu_new set sname='胡辣汤' where sno = 13"
    # ret = upd(sql)
    # print(ret)

    # sql = "delete from stu_new where sno = 13"
    # delete(sql)

    # sql = "select * from stu_new where sno = 9"
    # result = get_one(sql)
    # print(result)
    sql = "select * from stu_new"
    result = get_all(sql)
    print(result)

