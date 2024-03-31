from pymongo import MongoClient


def get_db():
    client = MongoClient(host="localhost", port=27017)  # 默认端口号: 27017
    # 我这里需要登录, 你们那不需要
    admin = client['admin']
    admin.authenticate("sylar", "123456")
    # 如果没有设置用户名密码, 直接切换就可以了
    db = client['syalr']   # use syalr
    return db


def add_one(collection_name, data):
    # 拿到db
    db = get_db()
    # result = db['teacher'].insert({"name": "alex", "age": 188})
    # result = db.teacher.insert({"name": "樵夫", "age":18})
    # result = db.collection_name.insert(data)  # 不能这么写
    result = db[collection_name].insert_one(data)
    print(result)
    return result


def add_many(collection_name, data):
    db = get_db()
    result = db[collection_name].insert_many(data)
    return result.inserted_ids


def upd(collection_name, condition, prepare):
    db = get_db()
    result = db[collection_name].update(condition, prepare, multi=True)
    return result


def delete(col, condition):
    db = get_db()
    db[col].delete_many(condition)


def query(col, condition):
    db = get_db()
    result = db[col].find(condition)
    return list(result)