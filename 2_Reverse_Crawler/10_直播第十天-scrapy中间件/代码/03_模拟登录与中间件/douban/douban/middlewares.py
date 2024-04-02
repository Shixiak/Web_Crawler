# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from douban.settings import USER_AGENT_LIST, PROXY_IP_LIST
from random import choice
from w3lib.http import basic_auth_header


class DoubanSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DoubanDownloaderMiddleware:

    def process_request(self, request, spider):
        ua = choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = ua
        return None  # 不能返回任何东西


# 免费代理
class ProxyDownloaderMiddleware:

    def process_request(self, request, spider):
        ip = choice(PROXY_IP_LIST)
        request.meta['proxy'] = "https://" + ip
        return None  # 放行

# 人民币玩家
class MoneyProxyDownloaderMiddleware:

    def process_request(self, request, spider):
        proxy = "tps138.kdlapi.com:15818"
        request.meta['proxy'] = f"http://{proxy}"
        # 用户名密码认证
        request.headers['Proxy-Authorization'] = basic_auth_header('t12831993520578', 't72a13xu')  # 白名单认证可注释此行
        request.headers["Connection"] = "close"
