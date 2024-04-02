
# 1. 可以选择先登录. 登录后.放慢抓取速度.
# 2. 不登录. 直接抓. 放慢抓取速度

from selenium.webdriver import Chrome
# 事件链
from selenium.webdriver.common.action_chains import ActionChains
# 显示等待
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By   # 提取页面内容的
from selenium.webdriver.support import expected_conditions as EC

from lxml import etree
import time
import json
import requests

#
# def base64_api(img, typeid=27, uname="q6035945", pwd="q6035945"):
#
#     data = {"username": uname, "password": pwd, "typeid": typeid, "image": img}
#     result = json.loads(
#         requests.post("http://api.ttshitu.com/predict", json=data).text
#     )
#     if result['success']:
#         return result["data"]["result"]
#     else:
#         return result["message"]
#
#
# web = Chrome()
# web.get("https://login.zhipin.com/?ka=header-login")
#
# web.implicitly_wait(10)
#
# web.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[1]/div[2]/div[1]/form/div[3]/span[2]/input').send_keys('18614075987')
# web.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[1]/div[2]/div[1]/form/div[4]/span/input').send_keys('123456789')
#
# web.find_element_by_xpath('//*[@id="pwdVerrifyCode"]/div').click()
#
# # 获取到验证码图片的div
# verify_div = web.find_element_by_xpath('/html/body/div[5]/div[2]/div[1]/div/div')
# verify_div.screenshot("tu.png")
# tu = verify_div.screenshot_as_base64  # 截图保存成b64的字符串
#
# verify_code = base64_api(tu)  # 开始识别
# print(verify_code)
#
# for p in verify_code.split("|"):  # 179,277|109,161
#     x = int(p.split(",")[0])
#     y = int(p.split(",")[1])
#     #                                                                              perform(): 提交事件
#     ActionChains(web).move_to_element_with_offset(verify_div, xoffset=x, yoffset=y).click().perform()
#     time.sleep(1)
#
#
# web.find_element_by_xpath('/html/body/div[5]/div[2]/div[1]/div/div/div[3]/a/div').click()
# time.sleep(2)
# web.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[1]/div[2]/div[1]/form/div[6]/button').click()



# 用selenium+lxml完成数据抓取

def get_page_source(url):
    web.get(url)

    # 显示等待
    el = WebDriverWait(web, 10, 0.5).until(  # until  结束等待的条件
        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[3]/ul/li[1]/div/div[1]/div[1]/div/div[1]/span[1]/a'))
    )
    page_source = web.page_source
    web.quit()
    return page_source


def get_job_name(page_source):
    tree = etree.HTML(page_source)
    job_names = tree.xpath('//*[@id="main"]/div/div[3]/ul/li/div/div[1]/div[1]/div/div[1]/span[1]/a/text()')
    print(job_names)


if __name__ == '__main__':
    web = Chrome()
    source = get_page_source("https://www.zhipin.com/job_detail/?query=python&city=101010100&industry=&position=")
    get_job_name(source)

