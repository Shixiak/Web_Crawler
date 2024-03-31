from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import json
import requests
import time


def base64_api(img, typeid=27, uname="q6035945", pwd="q6035945"):

    data = {"username": uname, "password": pwd, "typeid": typeid, "image": img}
    result = json.loads(
        requests.post("http://api.ttshitu.com/predict", json=data).text
    )
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]


# 如果你的浏览器版本是88以前, 要去执行一段js代码
# web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#   "source": """
#   navigator.webdriver = undefined
#     Object.defineProperty(navigator, 'webdriver', {
#       get: () => undefined
#     })
#   """
# })


# 88以后的版本用下面的方案
opt = Options()
opt.add_argument("--disable-blink-features=AutomationControlled")

web = Chrome(options=opt)

web.get("https://kyfw.12306.cn/otn/resources/login.html")

web.implicitly_wait(10)

# 切换到账号登录
web.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[2]/a').click()

web.find_element_by_xpath('//*[@id="J-userName"]').send_keys("18614075987")
web.find_element_by_xpath('//*[@id="J-password"]').send_keys("123456")

# 找到验证码图片位置
img = web.find_element_by_xpath('//*[@id="J-loginImg"]')
b64_verify_code = img.screenshot_as_base64

result = base64_api(b64_verify_code)

for p in result.split("|"):
    x = int(p.split(",")[0])
    y = int(p.split(",")[1])
    ActionChains(web).move_to_element_with_offset(img, x, y).click().perform()
    time.sleep(1)

# 点击登录按钮
web.find_element_by_xpath('//*[@id="J-login"]').click()

time.sleep(1)
btn = web.find_element_by_xpath('//*[@id="nc_1_n1z"]')

ActionChains(web).drag_and_drop_by_offset(btn, xoffset=300, yoffset=0).perform()
