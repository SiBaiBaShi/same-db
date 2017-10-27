# -*- coding: UTF-8 -*-
"""
2017.9.16
1.增加用户图片默认保存路径USER_PATH
2.默认更新频道删除“轻性感”
3.新增“这里只有帅哥美女”频道
2017.9.18
1.新增“晨间少女赏味期”和“短发控”频道
2.operate_sql函数增加出错控制
2017.9.19
1.去除operate_sql函数的差错控制
2.新增获取预设信息的get_info函数
3.新增“足控只是会欣赏美”、“比太阳还温暖的是你的笑”、“Masker-”和“单马尾即是正义_”频道
2017.9.20
1.增加operate_sql函数有关MySQL的异常处理
2.增加get_same_info函数requests请求的异常处理
"""
import json
import random
import time

import requests
import MySQLdb


INFO = r'C:\Users\root\Pictures\same\document\info.json'


def download_from_url(url, path):
    image = requests.get(url)
    with open(path, 'wb') as f:
        f.write(image.content)


def get_info(key):
    with open(INFO) as f:
        info = json.loads(f.read())
    return info[key]


def get_same_info(url):

    def headers():

        def union_id():
            def gen_id(length):
                chars = ['a', 'b', 'c', 'd', 'e', 'f',
                         '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
                array = ''
                while length is not 0:
                    array += random.choice(chars)
                    length -= 1
                return array

            ids = [gen_id(8), gen_id(4), gen_id(4), gen_id(4), gen_id(12)]
            return '-'.join(ids).lower()

        header = {
            'X-Same-Request-ID': union_id(),
            'X-same-Client-Version': '593',
            'Machine': 'android|301|android6.0.1|Redmi 3S|d:863316375146|720|1280',
            'Host': 'im-xs.same.com',
            'X-same-Device-UUID': 'd:863316375146',
            'PACKAGE-NAME': 'com.same.android',
            'User-Agent': 'same/593',
            'Connection': 'keep-alive',
            'Advertising-UUID': 'd:863316375146',
            'timezone': 'Asia/Shanghai',
            'Authorization': 'Token 1500806062-PZ12MW6jmh8W1nn2-15974677',
            'Extrainfo': 'yingyongbao',
            'Accept-Encoding': 'gzip'
        }
        return header

    status = 1
    while status:
        try:
            response = requests.get(url=url, headers=headers())
        except requests.ConnectionError, e:
            print e
            time.sleep(60)
        except requests.HTTPError, e:
            print e
            time.sleep(0.1)
        else:
            return response


def operate_sql(db, sql):
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        temp = cursor.fetchall()
        cursor.close()
        return temp
    except MySQLdb.Error, e:
        try:
            print "Error %d:%s" % (e.args[0], e.args[1])
            print sql
        except IndexError:
            print "MySQL Error:%s" % str(e)
            print sql
