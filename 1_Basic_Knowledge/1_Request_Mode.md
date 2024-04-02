# Request_Mode

## Get请求



## Post请求

```Python
import requests

url = "https://fanyi.baidu.com/sug"

# post请求的参数是通过data传递的
data = {
    "kw": input("请输入一个单词")
}

resp = requests.post(url, data=data)

print(resp.text)  # 拿到的是文本字符串
print(resp.json())  # 此时拿到的直接是json数据
```