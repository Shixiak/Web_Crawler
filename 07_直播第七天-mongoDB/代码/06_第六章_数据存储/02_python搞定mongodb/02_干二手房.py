import requests
from lxml import etree
from mongodb import add_many  # pycharm误报
import pymysql


def get_page_source(url):
    resp = requests.get(url)
    page_source = resp.text
    return page_source


def parse(html):
    tree = etree.HTML(html)
    li_list = tree.xpath("//ul[@class='sellListContent']/li")
    result = []
    for li in li_list:

        title = li.xpath("./div[1]/div[1]/a/text()")[0]

        position = "-".join(li.xpath("./div[1]/div[2]/div[1]/a/text()")).replace(" ", "")
        house = li.xpath("./div[1]/div[3]/div[1]/text()")[0]
        house = house.split(" | ")
        if len(house) == 6:  # 有些数据没有年份
            house.insert(5, "")
        if len(house) == 8:
            house.pop()  # 有些数据是"别墅", 弹出去

        # 直接解构成变量
        huxing, mianji, chaoxiang, zhuangxiu, louceng, nianfen, jiegou = house

        tags = li.xpath("./div[1]/div[5]/span/text()")
        dic = {
            "title": title,
            "position": position,
            "huxing": huxing,
            "mianji": mianji,
            "chaoxiang": chaoxiang,
            "zhuangxiu": zhuangxiu,
            "louceng": louceng,
            "nianfen": nianfen,
            "jiegou": jiegou,
            "tags": tags
        }
        result.append(dic)
    return result


def save_to_mongo(data_list):
    add_many("ershoufang", data_list)
    print("一页保存完毕")


def save_to_mysql(data_list):
    try:
        conn = pymysql.connect(host="localhost", port=3306, user="root", password="test123456", database="spider")
        cursor = conn.cursor()

        # 这里面的%s只是占位
        sql = "insert into ershoufang(title,position,huxing,mianji,chaoxiang,zhuangxiu,louceng,nianfen,jiegou,tags) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # 处理一下tags
        for dic in data_list:
            dic['tags'] = ",".join(dic['tags'])

        # 将数据存储成[(), (), ()]
        lst = (tuple(dic.values()) for dic in data_list)

        cursor.executemany(sql, lst)
        conn.commit()
    except:
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    for i in range(1, 31):
        url = f"https://bj.lianjia.com/ershoufang/pg{i}/"
        page_source = get_page_source(url)
        data_list = parse(page_source)
        # 存储数据
        # save_to_mongo(data_list)
        save_to_mysql(data_list)