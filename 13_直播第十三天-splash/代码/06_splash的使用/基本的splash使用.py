import requests
from lxml import etree
"""
# splash提供的api接口
渲染html的接口
http://192.168.31.184:8050/render.html?url=你的url&wait=等待时间&time_out=超时时间

截图的接口
http://192.168.31.184:8050/render.png  参数和render.html基本一致, 可选width, height

加载过程接口
http://192.168.31.184:8050/render.har  参数和render.html基本一致

json接口
http://192.168.31.184:8050/render.json  参数和render.html基本一致

执行lua脚本的接口
http://192.168.31.184:8050/execute?lua_source=你要执行的lua脚本
"""

# resp = requests.get(url="http://192.168.31.172:8050/render.html", params={
#     "url": "https://www.endata.com.cn/BoxOffice/BO/Year/index.html",  # 你要渲染的url
#     "wait": 10  # time.sleep(10)
# })
#
# print(resp.text)


# 抓取网易新闻
lua_source = """
function main(splash, args)
  assert(splash:go("https://news.163.com/"))
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
#
# resp = requests.get(url="http://192.168.31.172:8050/execute", params={
#     "lua_source": lua_source
# })
#
# tree = etree.HTML(resp.text)
#
# divs = tree.xpath("//ul[@class='newsdata_list fixed_bar_padding noloading']/li[1]/div[2]/div")
# for div in divs:
#     a = div.xpath("./div/div/h3/a")
#     if not a:  # 过滤掉广告
#         continue
#     a = a[0]
#     print(a.xpath("./@href"))
#     print(a.xpath("./text()"))


