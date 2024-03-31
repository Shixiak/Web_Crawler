# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import pymysql
from tupianzhijia.settings import MYSQL
import scrapy


class TupianzhijiaPipeline:
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host=MYSQL['host'],
            port=MYSQL['port'],
            user=MYSQL['user'],
            password=MYSQL['password'],
            database=MYSQL['database']
        )

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        try:
            cursor = self.conn.cursor()
            sql = "insert into tu (name, img_src, local_path) values (%s, %s, %s)"
            cursor.execute(sql, (item['name'], item['img_src'], item['local_path']))
            self.conn.commit()
        except:
            self.conn.rollback()
        finally:
            if cursor:
                cursor.close()
        return item


# 想要使用ImagesPipeline 必须单独设置一个配置, 用来保存文件的文件夹
class MeinvSavePipeline(ImagesPipeline):  # 利用图片管道帮我们完成数据下载操作

    def get_media_requests(self, item, info):  # 负责下载的
        yield scrapy.Request(item['img_src'])  # 直接返回一个请求即可

    def file_path(self, request, response=None, info=None):  # 准备文件路径
        file_name = request.url.split("/")[-1]  # request.url可以直接获取到刚刚请求的url
        return f"img/{file_name}"  # img/xxx.jpg

    def item_completed(self, results, item, info):  # 返回文件的详细信息
        ok, finfo = results[0]
        item['local_path'] = finfo["path"]
        return item
