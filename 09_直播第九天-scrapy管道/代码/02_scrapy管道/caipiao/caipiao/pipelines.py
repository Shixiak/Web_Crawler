# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import pymongo
from caipiao.settings import MYSQL

"""
存储数据的方案:
    1. 数据要存储在csv文件中
    2. 数据存储在mysql数据库中
    3. 数据存储在mongodb数据库中
    4. 文件的存储
"""


class CaipiaoPipeline:

    """
    我们希望的是, 在爬虫开始的时候. 打开这个文件
    在执行过程中. 不断的往里存储数据
    在执行完毕时, 关掉这个文件
    """
    def open_spider(self, spider):
        self.f = open("./双色球.csv", mode="a", encoding="utf-8")

    def close_spider(self,  spider):
        if self.f:
            self.f.close()

    def process_item(self, item, spider):
        self.f.write(f"{item['qihao']},{'_'.join(item['red_ball'])},{item['blue_ball']}\n")
        return item


class CaipiaoMySQLPipeline:

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host=MYSQL['host'],
            port=MYSQL['port'],
            user=MYSQL['user'],
            password=MYSQL['password'],
            database=MYSQL['database']
        )

    def close_spider(self,  spider):
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        try:
            cursor = self.conn.cursor()
            sql = "insert into caipiao (qihao, red_ball, blue_ball) values (%s, %s, %s)"
            cursor.execute(sql, (item['qihao'], "_".join(item['red_ball']), item['blue_ball']))
            self.conn.commit()
        except:
            self.conn.rollback()
        finally:
            if cursor:
                cursor.close()
        return item


class CaipiaoMongoDBPipeline:

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host="localhost", port=27017)
        db = self.client['python']  # use database
        db.authenticate("python_admin", "123456")
        self.collection = db['caipiao2']  # 指定彩票集合

    def close_spider(self,  spider):
        self.client.close()

    def process_item(self, item, spider):
        self.collection.insert({"qihao": item['qihao'], "red_ball": item['red_ball'], "blue_ball": item['blue_ball']})
        return item
