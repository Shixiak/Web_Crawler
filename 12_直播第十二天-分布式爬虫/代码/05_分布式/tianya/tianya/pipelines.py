# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TianyaPipeline:
    def process_item(self, item, spider):
        # 判断. 是否在redis里面已经存储了. 如果存储了就不进入数据库,
        print("我要存储到数据库了", item)
        return item
