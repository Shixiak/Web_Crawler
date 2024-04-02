from selenium.webdriver import Chrome
from selenium.webdriver.support.select import Select  # 下拉列表 <select>
import time

# 配置无头信息
from selenium.webdriver.chrome.options import Options

opt = Options()
opt.add_argument("--headless")
opt.add_argument("--disable-gpu")

web = Chrome(options=opt)

web.get("https://www.endata.com.cn/BoxOffice/BO/Year/index.html")

sel = web.find_element_by_xpath('//*[@id="OptionDate"]')
sel_new = Select(sel)

print(len(sel_new.options))  # 所有的选项 0 1 2 3 4 5 6
for i in range(len(sel_new.options)):
    sel_new.select_by_index(i)  # 根据位置切换
    time.sleep(3)  # 切换完毕等待加载数据
    # 切换完了之后.
    trs = web.find_elements_by_xpath('//*[@id="TableList"]/table/tbody/tr')
    for tr in trs:
        print(tr.text)

# # 获取页面代码( 不是页面源代码, 是F12里面 elements的代码)
# page_source = web.page_source
# print(page_source)
