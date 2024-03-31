from selenium import webdriver
from chaojiying import Chaojiying_Client  # 写完代码后. 一定要把前面那个.干掉

web = webdriver.Chrome()
web.get("https://www.chaojiying.com/user/login/")


png = web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/div/img').screenshot_as_png

chaojiying = Chaojiying_Client('18614075987', 'q6035945', '919889')
result = chaojiying.PostPic(png, 1902)
v_code = result['pic_str']


web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/p[3]/input').send_keys(v_code)
web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/p[1]/input').send_keys("18614075987")
web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/p[2]/input').send_keys("q6035945")
web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/p[4]/input').click()
