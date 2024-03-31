# selenium可以自动打开一个浏览器.
# 输入网址.
# 能从页面里提取东西
# 先确定打开的是哪个浏览器 -> Chrome

from selenium.webdriver import Chrome


# 创建浏览器对象
# executable_path: 指定浏览器驱动的路径
# web = Chrome(executable_path="./chromedriver")
web = Chrome()  # 此时自动查找浏览器驱动

url = "http://www.baidu.com"

# 打开该url对应的网址
web.get(url)

print(web.title)  # 固定的. 获取到网站的titile标签中的内容
