from redis import Redis

r = Redis(host='localhost',
          port=6379,
          db=3,
          password="123456",
          decode_responses=True)  # 相当于 --raw  不看字节了

# set key value
# r.set("name", "渣渣辉")

# # get key
# result = r.get("name")
# print(result)

# zadd key f1 d1 f2 d2 f3 d3
# r.zadd("xiangyan", {"宇宙香烟": 10, "紫云": 11, "不知道啊": 15})

# zincrby key fen data
r.zincrby("xiangyan", -5, "紫云")
