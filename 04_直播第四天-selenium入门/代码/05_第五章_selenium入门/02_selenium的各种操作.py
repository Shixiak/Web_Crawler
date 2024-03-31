# 目标: 拉钩网的招聘信息
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import time

web = Chrome()
web.get("http://www.lagou.com")


# 找到页面中的x. 点击它
x_btn = web.find_element_by_xpath('//*[@id="cboxClose"]')  # 根据xpaht定位页面元素,  copy xpath 只能在selenium环境下放心大胆的用.
x_btn.click()

# 找到 输入框. "输入python 回车"  或者  "输入python 点击搜索"
# 休息一下下
time.sleep(1)
web.find_element_by_xpath('//*[@id="search_input"]').send_keys("python", Keys.ENTER)

time.sleep(2)

# selenium可以动态执行js
web.execute_script("""
    var a = document.getElementsByClassName("un-login-banner")[0];
    a.parentNode.removeChild(a);
""")
# 数据提取                             //*[@id="s_position_list"]/ul/li[6]/div[1]/div[1]/div[1]/a/h3
li_list = web.find_elements_by_xpath('//*[@id="s_position_list"]/ul/li')

for li in li_list:
    h3 = li.find_element_by_xpath("./div[1]/div[1]/div[1]/a/h3")
    h3.click()
    # 此时, 在浏览器这边. 我们看到的内容已经是详情页的内容了.
    # 但是, 在selenium的眼中. 我们依然在首页.
    # 所以, 必须得让selenium去调整它的视角
    # 切换窗口
    web.switch_to.window(web.window_handles[-1])
    job_detail = web.find_element_by_xpath('//*[@id="job_detail"]/dd[2]/div')
    txt = job_detail.text
    print(txt)
    time.sleep(1)  # 节奏慢一点儿
    # 关闭该窗口
    web.close()
    # 调整selenium的视角
    web.switch_to.window(web.window_handles[0])

web.quit()  # 关闭浏览器



