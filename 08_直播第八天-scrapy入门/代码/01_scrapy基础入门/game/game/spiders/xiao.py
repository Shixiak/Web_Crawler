import scrapy


class XiaoSpider(scrapy.Spider):
    name = 'xiao'   # 爬虫名字
    allowed_domains = ['4399.com']  # 允许的域名
    start_urls = ['http://www.4399.com/flash/']  # 起始页面url


    def parse(self, response):  # 该方法默认是用来处理解析的
        # 本来应该是解析数据的
        # print(response)
        # 拿到页面源代码
        # print(response.text)
        # 提取数据
        # response.json()
        # response.xpath()  # 用xpath进行数据解析
        # response.css()   # 用css选择器进行解析

        # 获取到页面中所有的游戏名字
        # txt = response.xpath("//ul[@class='n-game cf']/li/a/b/text()").extract()  # 提取内容
        # print(txt)

        # 分块提取数据
        li_list = response.xpath("//ul[@class='n-game cf']/li")
        for li in li_list:
            name = li.xpath("./a/b/text()").extract_first()  # extract_first提取一项内容, 如果没有, 返回None
            categroy = li.xpath("./em/a/text()").extract_first()
            date = li.xpath("./em/text()").extract_first()

            dic = {
                "name": name,
                "categroy": categroy,
                "date": date
            }
            # 需要用yield将数据传递给管道
            yield dic  # 如果返回的是数据. 直接可以认为是给了管道pipeline
