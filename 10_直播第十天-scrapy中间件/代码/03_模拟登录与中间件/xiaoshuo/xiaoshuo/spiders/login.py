import scrapy


class LoginSpider(scrapy.Spider):  # 子类对父类提供的某个方法不满意了.不满足了. 重写它即可
    name = 'login'
    allowed_domains = ['17k.com']
    start_urls = ['https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919']
    """
        需要重新定义一下. scrapy原来对于start_urls的处理
        只需要重写start_requests()方法即可. 
    """
    def start_requests(self):

        # # 直接从浏览器复制cookie信息
        # cookie_str = """
        # GUID=bbb5f65a-2fa2-40a0-ac87-49840eae4ad1; c_channel=0; c_csc=web; accessToken=avatarUrl%3Dhttps%253A%252F%252Fcdn.static.17k.com%252Fuser%252Favatar%252F16%252F16%252F64%252F75836416.jpg-88x88%253Fv%253D1610625030000%26id%3D75836416%26nickname%3D%25E5%25AD%25A4%25E9%25AD%2582%25E9%2587%258E%25E9%25AC%25BCsb%26e%3D1643699303%26s%3De6dacaa919cc8686; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2275836416%22%2C%22%24device_id%22%3A%2217700ba9c71257-035a42ce449776-326d7006-2073600-17700ba9c728de%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22bbb5f65a-2fa2-40a0-ac87-49840eae4ad1%22%7D; Hm_lvt_9793f42b498361373512340937deb2a0=1627711457,1627898858,1628144975,1628333752; Hm_lpvt_9793f42b498361373512340937deb2a0=1628337972
        # """
        # lst = cookie_str.split("; ")
        # dic = {}
        # for it in lst:
        #     k, v = it.split("=")
        #     dic[k.strip()] = v.strip()
        #
        # yield scrapy.Request(
        #     url=LoginSpider.start_urls[0],
        #     cookies=dic
        # )

        # 走登录流程
        url = "https://passport.17k.com/ck/user/login"
        username = "17673842014"
        password = "lx0609"
        # 发送post请求的第一个方案(不好)
        # yield scrapy.Request(
        #     url=url,
        #     method='post',
        #     body=f"loginName={username}&password={password}",
        #     callback=self.parse
        # )
        # 发送post的第二个方案(常用)
        yield scrapy.FormRequest(
            url=url,
            formdata={
                "loginName": username,
                "password": password
            },
            callback=self.parse
        )

    def parse(self, response):
        yield scrapy.Request(url=LoginSpider.start_urls[0], callback=self.parse_detail)

    def parse_detail(self, resp):
        print(resp.text)
