import scrapy
from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider
from tianya2.items import TianyaItem


class TySpider(RedisSpider):  # 换成RedisSpider
    name = 'ty'
    allowed_domains = ['tianya.cn']
    # start_urls = ['http://tianya.cn/']  # 注释掉
    redis_key = "ty_start_url"   # 换成redis_key

    def parse(self, resp, **kwargs):
        # 进入详情页
        tbodys = resp.xpath("//table[@class='tab-bbs-list tab-bbs-list-2']/tbody")[1:]
        for tbody in tbodys:
            hrefs = tbody.xpath("./tr/td[1]/a/@href").extract()
            for href in hrefs:
                detail_url = resp.urljoin(href)
                # 这里不用管是否重复. 所有的判断工作. 全部交给scrapy_redis完成
                yield scrapy.Request(
                    url=detail_url,
                    callback=self.parse_detail,
                )

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
        yield t

