from selenium.webdriver import Chrome

web = Chrome()
web.get("http://www.baidu.com")

cookies = web.get_cookies()
print(cookies)
# a=jlkfjadslkfjklasdjfklsadjkfljasdfasj;b=fkldsjaklfjadskljfklasdjfklasdjfkads;c=flkdsajkfljaskdljdfk
# { 'name': 'BAIDUID_BFESS', 'value': '54C6C2D26FD40BA3E1ED915BAFEE0C10:FG=1'}
# # BAIDUID_BFESS=54C6C2D26FD40BA3E1ED915BAFEE0C10:FG=1
# {
#     "BAIDUID_BFESS": "54C6C2D26FD40BA3E1ED915BAFEE0C10:FG=1"
# }
cookie_dic = {}
for dic in cookies:
    key = dic['name']
    value = dic['value']
    cookie_dic[key] = value
print(cookie_dic)

cookie_dic = {dic['name']: dic['value'] for dic in cookies}  # 字典生成式 -> 列表生成式

# 当你已经有了一个字典形式的cookie, 可以直接把这个字典作为参数传递给requests
import requests

headers = {

}                                   # 直接把cookies当成参数传递即可(必须是字典)
requests.get("xxxx", headers=headers, cookies=cookie_dic)
