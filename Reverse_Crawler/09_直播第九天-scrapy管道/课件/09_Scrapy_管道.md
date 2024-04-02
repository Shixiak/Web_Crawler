# Scrapy管道



在上一小节中, 我们初步掌握了Scrapy的基本运行流程以及基本开发流程. 本节继续讨论关于Scrapy更多的内容. 

## 一. 关于管道

上一节内容, 我们已经可以从spider中提取到数据. 然后通过引擎将数据传递给pipeline, 那么在pipeline中如何对数据进行保存呢? 我们主要针对四种数据存储展开讲解. 

前三个案例以http://datachart.500.com/ssq/为案例基础. 最后一个以https://www.tupianzj.com/bizhi/DNmeinv/为案例基础. 

### 1. csv文件写入

​		写入文件是一个非常简单的事情. 直接在pipeline中开启文件即可. 但这里要说明的是. 如果我们只在process_item中进行处理文件是不够优雅的.  总不能有一条数据就open一次吧

```python
class CaipiaoFilePipeline:
    
    def process_item(self, item, spider):
        with open("caipiao.txt", mode="a", encoding='utf-8') as f:
            # 写入文件
            f.write(f"{item['qihao']}, {'_'.join(item['red_ball'])}, {'_'.join(item['blue_ball'])}\n")
        return item
```

​		我们希望的是, 能不能打开一个文件, 然后就用这一个文件句柄来完成数据的保存. 答案是可以的. 我们可以在pipeline中创建两个方法, 一个是open_spider(), 另一个是close_spider(). 看名字也能明白其含义: 

​		open_spider(), 在爬虫开始的时候执行一次
​		close_spider(), 在爬虫结束的时候执行一次

​		有了这俩货, 我们就可以很简单的去处理这个问题

```python
class CaipiaoFilePipeline:

    def open_spider(self, spider):
        self.f = open("caipiao.txt", mode="a", encoding='utf-8')

    def close_spider(self, spider):
        if self.f:
            self.f.close()

    def process_item(self, item, spider):
        # 写入文件
        self.f.write(f"{item['qihao']}, {'_'.join(item['red_ball'])}, {'_'.join(item['blue_ball'])}\n")
        return item
```

​		在爬虫开始的时候打开一个文件, 在爬虫结束的时候关闭这个文件. 满分~

​		对了, 别忘了设置settings

```python
ITEM_PIPELINES = {
   'caipiao.pipelines.CaipiaoFilePipeline': 300,
}
```



### 2. mysql数据库写入

​		有了上面的示例, 写入数据库其实也就很顺其自然了, 首先, 在open_spider中创建好数据库连接. 在close_spider中关闭链接. 在proccess_item中对数据进行保存工作. 

先把mysql相关设置丢到settings里

```python
# MYSQL配置信息
MYSQL_CONFIG = {
   "host": "localhost",
   "port": 3306,
   "user": "root",
   "password": "test123456",
   "database": "spider",
}
```



```python
from caipiao.settings import MYSQL_CONFIG as mysql
import pymysql

class CaipiaoMySQLPipeline:

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=mysql["host"], port=mysql["port"], user=mysql["user"], password=mysql["password"], database=mysql["database"])

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        # 写入文件
        try:
            cursor = self.conn.cursor()
            sql = "insert into caipiao(qihao, red, blue) values(%s, %s, %s)"
            red = ",".join(item['red_ball'])
            blue = ",".join(item['blue_ball'])
            cursor.execute(sql, (item['qihao'], red, blue))
            self.conn.commit()
            spider.logger.info(f"保存数据{item}")
        except Exception as e:
            self.conn.rollback()
            spider.logger.error(f"保存数据库失败!", e, f"数据是: {item}")  # 记录错误日志
        return item

```

别忘了把pipeline设置一下

```python
ITEM_PIPELINES = {
   'caipiao.pipelines.CaipiaoMySQLPipeline': 301,
}
```



### 3. mongodb数据库写入

​		mongodb数据库写入和mysql写入如出一辙...不废话直接上代码吧

```python
MONGO_CONFIG = {
   "host": "localhost",
   "port": 27017,
   'has_user': True,
   'user': "python_admin",
   "password": "123456",
   "db": "python"
}
```



```python
from caipiao.settings import MONGO_CONFIG as mongo
import pymongo

class CaipiaoMongoDBPipeline:
    def open_spider(self, spider):
        client = pymongo.MongoClient(host=mongo['host'],
                                     port=mongo['port'])
        db = client[mongo['db']]
        if mongo['has_user']:
            db.authenticate(mongo['user'], mongo['password'])
        self.client = client
        self.collection = db['caipiao']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.collection.insert({"qihao": item['qihao'], 'red': item["red_ball"], 'blue': item['blue_ball']})
        return item
```

```python
ITEM_PIPELINES = {
    # 三个管道可以共存~
   'caipiao.pipelines.CaipiaoFilePipeline': 300,
   'caipiao.pipelines.CaipiaoMySQLPipeline': 301,
   'caipiao.pipelines.CaipiaoMongoDBPipeline': 302,
}
```



### 4. 文件保存

接下来我们来尝试使用scrapy来下载一些图片, 看看效果如何. 

首先, 随便找个图片网站(安排好的). https://www.tupianzj.com/bizhi/DNmeinv/. 可以去看看, 妹子们还是很漂亮的. 

接下来. 创建好项目,  定义好数据结构

```python
class MeinvItem(scrapy.Item):
    name = scrapy.Field()
    img_url = scrapy.Field()
    img_path = scrapy.Field()
```



完善spider, 注意看yield scrapy.Request()

```python
import scrapy
from meinv.items import MeinvItem


class TupianzhijiaSpider(scrapy.Spider):
    name = 'tupianzhijia'
    allowed_domains = ['tupianzj.com']
    start_urls = ['https://www.tupianzj.com/bizhi/DNmeinv/']

    def parse(self, resp, **kwargs):
        li_list = resp.xpath("//ul[@class='list_con_box_ul']/li")
        for li in li_list:
            href = li.xpath("./a/@href").extract_first()
            # 拿到href为了什么? 进入详情页啊
            """
            url: 请求地址
            method: 请求方式
            callback: 回调函数
            errback: 报错回调
            dont_filter: 默认False, 表示"不过滤", 该请求会重新进行发送
            headers: 请求头. 
            cookies: cookie信息
            """
            yield scrapy.Request(
                url=resp.urljoin(href),  # scrapy的url拼接
                method='get',
                callback=self.parse_detail,
            )
        # 下一页
        next_page = resp.xpath('//div[@class="pages"]/ul/li/a[contains(text(), "下一页")]/@href').extract_first()
        if next_page:
            yield scrapy.Request(
                url=resp.urljoin(next_page),
                method='get',
                callback=self.parse
            )


    def parse_detail(self, resp):
        img_src = resp.xpath('//*[@id="bigpic"]/a[1]/img/@src').extract_first()
        name = resp.xpath('//*[@id="container"]/div/div/div[2]/h1/text()').extract_first()
        meinv = MeinvItem()
        meinv['name'] = name
        meinv['img_url'] = img_src
        yield meinv
        
```

​		关于Request()的参数:
​			url: 请求地址
​            method: 请求方式
​            callback: 回调函数
​            errback: 报错回调
​            dont_filter: 默认False, 表示"不过滤", 该请求会重新进行发送
​            headers: 请求头. 
​            cookies: cookie信息

​		接下来就是下载问题了. 如何在pipeline中下载一张图片呢? Scrapy早就帮你准备好了. 在Scrapy中有一个ImagesPipeline可以实现自动图片下载功能. 

```python
from scrapy.pipelines.images import ImagesPipeline, FilesPipeline
import pymysql
from meinv.settings import MYSQL
import scrapy

class MeinvPipeline:
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
            sql = "insert into tu (name, img_src, img_path) values (%s, %s, %s)"
            cursor.execute(sql, (item['name'], item['img_src'], item['img_path']))
            self.conn.commit()
        except:
            self.conn.rollback()
        finally:
            if cursor:
                cursor.close()
        return item


class MeinvSavePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # 发送请求去下载图片
        # 如果是一堆图片. 可以使用循环去得到每一个url, 然后在yield每一个图片对应的Request对象
        return scrapy.Request(item['img_url'])

    def file_path(self, request, response=None, info=None):
        # 准备好图片的名称
        filename = request.url.split("/")[-1]
        return f"img/{filename}"

    def item_completed(self, results, item, info):
        # 文件存储的路径
        ok, res = results[0]
        # print(res['path'])
        item['img_path'] = res["path"]
        return item
```

最后, 需要在settings中设置以下内容:

```python
MYSQL = {
   "host": "localhost",
   "port": 3306,
   "user": "root",
   "password": "test123456",
   "database": 'spider'
}

ITEM_PIPELINES = {
    'meinv.pipelines.MeinvPipeline': 303,
    'meinv.pipelines.MeinvSavePipeline': 301,
}
# 图片保存路径  -> ImagesPipeline
IMAGES_STORE= './my_tu'
# 文件保存路径 -> FilesPipeline
FILES_STORE = './my_tu'
```

