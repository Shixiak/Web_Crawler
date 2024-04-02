import scrapy
from scrapy_splash.request import SplashRequest
from scrapy_redis.spiders import RedisSpider
from news.items import NewsItem

lua_source = """
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(2))
  -- 准备一个js函数. 预加载
  -- jsfunc是splash预留的专门为了js代码和lua代码结合准备的
  get_btn_display = splash:jsfunc([[
    	function(){
    		return document.getElementsByClassName('load_more_btn')[0].style.display;
  		}
    ]])

  while(true)
  do
    splash:runjs("document.getElementsByClassName('load_more_btn')[0].scrollIntoView(true)")
    splash:select(".load_more_btn").click()
    splash:wait(1)
    -- 判断load_more_btn是否是none.
    display = get_btn_display()
    if(display == 'none')
      then
        break
      end
  end

  return splash:html()  -- 直接返回页面源代码
end
"""


class WangyiSpider(RedisSpider):
    name = 'wangyi'
    allowed_domains = ['163.com']
    # redis_key = "wangyi:news:start_urls"
    start_urls = ['https://news.163.com/']
    # 重写start_request, 这地方由于重写了start_request, 就不需要redis_key了
    def start_requests(self):
        yield SplashRequest(
            url=self.start_urls[0],
            callback=self.parse,
            endpoint="execute",  # 终端表示你要执行哪一个splash的服务
            args={
                "lua_source": lua_source
            },
            dont_filter=True   # 不去重. 直接进队列
        )

    def parse(self, response):
        divs = response.xpath("//ul[@class='newsdata_list fixed_bar_padding noloading']/li[1]/div[2]/div")
        for div in divs:
            a = div.xpath("./div/div/h3/a")
            if not a:  # 过滤掉广告
                continue
            a = a[0]
            xw = NewsItem()
            xw['url'] = a.xpath("./@href").extract_first()
            xw['title'] = a.xpath("./text()").extract_first()
            yield xw
            print(1)
            yield scrapy.Request(
                url=xw['url'],
            )


