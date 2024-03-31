import base64
import json
import requests
# 一、图片文字类型(默认 3 数英混合)：
# 1 : 纯数字
# 1001：纯数字2
# 2 : 纯英文
# 1002：纯英文2
# 3 : 数英混合
# 1003：数英混合2
#  4 : 闪动GIF
# 7 : 无感学习(独家)
# 11 : 计算题
# 1005:  快速计算题
# 16 : 汉字
# 32 : 通用文字识别(证件、单据)
# 66:  问答题
# 49 :recaptcha图片识别 参考 https://shimo.im/docs/RPGcTpxdVgkkdQdY
# 二、图片旋转角度类型：
# 29 :  旋转类型
#
# 三、图片坐标点选类型：
# 19 :  1个坐标
# 20 :  3个坐标
# 21 :  3 ~ 5个坐标
# 22 :  5 ~ 8个坐标
# 27 :  1 ~ 4个坐标
# 48 : 轨迹类型
#
# 四、缺口识别
# 18 : 缺口识别（需要2张图 一张目标图一张缺口图）
# 33 : 单缺口识别（返回X轴坐标 只需要1张图）
# 五、拼图识别
# 53：拼图识别


def base64_api(uname, pwd, img, typeid):
    # with open(img, mode='rb') as f:
    #     base64_data = base64.b64encode(f.read())  # f.read()字节 => b64字符串
    #     b64 = base64_data.decode()  # b64是字符串(图片)

    data = {"username": uname, "password": pwd, "typeid": typeid, "image": img}
    result = json.loads(
        requests.post("http://api.ttshitu.com/predict", json=data).text
    )
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]


# requests + 图鉴
def login():
    # 请求到图片的地址, 提取到图片的b64以及图片的imgId

    verify_url = "http://admin.ttshitu.com/captcha_v2"
    session = requests.session()
    resp = session.get(verify_url)
    img = resp.json()

    # 开始识别
    result = base64_api("q6035945", "q6035945", img['img'], 3)
    print(result)

    login_url = "http://admin.ttshitu.com/common/api/login/user"  # POST
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }

    data = {
        "captcha": result,  # 验证码
        "imgId": img['imgId'],  # ???
        "developerFlag": False,
        "needCheck": True,
        "password": "q6035945",
        "userName": "q6035945"
    }
    resp = session.post(login_url, json=data)
    print(resp.text)


if __name__ == "__main__":
    login()
