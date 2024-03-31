import scrapy
from scrapy.spiders import Spider
from tianya.items import TianyaItem
from redis import Redis


class TySpider(scrapy.Spider):
    name = 'ty'
    allowed_domains = ['tianya.cn']
    start_urls = ['http://bbs.tianya.cn/list-worldlook-1.shtml']

    def __init__(self, name=None, **kwargs):
        self.red = Redis(host="127.0.0.1", port=6379, db=9, password="123456")
        # 让父类能初始化
        super(TySpider, self).__init__(name, **kwargs)

    def parse(self, resp, **kwargs):
        # 进入详情页
        tbodys = resp.xpath("//table[@class='tab-bbs-list tab-bbs-list-2']/tbody")[1:]
        for tbody in tbodys:
            hrefs = tbody.xpath("./tr/td[1]/a/@href").extract()
            for href in hrefs:
                detail_url = resp.urljoin(href)
                # 1.直接往redis里set集合怼.
                # 进入到详情页的条件是: 我在redis里面没有存储过该url
                # 2.在这里判断是否存在该元素
                result = self.red.sismember("tianya:ty:detail:url", detail_url)
                if result:
                    print(f"该url已经被抓取过{detail_url}")
                else:
                    yield scrapy.Request(
                        url=detail_url,
                        callback=self.parse_detail,
                    )

        # 天涯现在还有人吗？记得好多年前，天天都要逛天涯，现在成这样了
        # 阿富汗塔利班说已攻占萨曼甘省首府艾巴克市
        # 阿富汗塔利班说已攻占萨曼甘省首府艾巴克市
        # 有重复的数据产生了.
        # 如何来进行去除重复的问题
        # 1. 使用python的set集合来去重.
        # 2. 推荐使用redis的set集合去除重复
        # 用redis有两个方案去除重复
        # 1. url , 优点: 简单, 缺点. 如果url内部进行了更新. 你可能会忽略掉一些数据
        # 2. 数据 , 优点: 准确性高,  缺点. 如果数据集非常庞大. 对于redis而言是很不利的.


        # 可以考虑继续爬取下一页的信息
        next_href = resp.xpath("//div[@class='short-pages-2 clearfix']/div/a[last()]/@href").extract_first()
        yield scrapy.Request(
            url=resp.urljoin(next_href),
            callback=self.parse
        )

    def parse_detail(self, resp, **kwargs):
        t = TianyaItem()
        title = resp.xpath('//*[@id="post_head"]/h1/span[1]/span/text()').extract_first()
        content = resp.xpath('//*[@id="bd"]/div[4]/div[1]/div/div[2]/div[1]/text()').extract_first()
        t['title'] = title.strip()
        t['content'] = content.strip()
        self.red.sadd("tianya:ty:detail:url", resp.url)
        yield t



