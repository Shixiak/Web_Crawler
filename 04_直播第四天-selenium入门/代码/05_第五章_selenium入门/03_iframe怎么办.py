from selenium.webdriver import Chrome


web = Chrome()
web.get("http://www.wbdy.tv/play/30288_1_1.html")

# 切换到iframe
iframe = web.find_element_by_xpath('//*[@id="mplay"]')
web.switch_to.frame(iframe)  # 切换到iframe里面

input = web.find_element_by_xpath('//*[@id="dplayer"]/div[4]/div[1]/input')
placeholder = input.get_property('placeholder')
print(placeholder)

# 跳出iframe怎么办??
web.switch_to.parent_frame()
content = web.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div/div[2]/p[1]').text
print(content)
