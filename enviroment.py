# -*- coding: UTF-8 -*-
"""
啊
"""
import json
import random
import re
import time

import requests


INFO = r'C:\Users\root\Pictures\same\document\info.json'
PATH = r'C:\Users\root\Pictures\same\download\\'


def download_from_url(url, path):
    image = requests.get(url)
    with open(path, 'wb') as f:
        f.write(image.content)


def get_channel_info():
    """
    :return:{ids{(文件名:id),}, names{文件名1,文件名2], urls(id:url,)}
    """
    with open(INFO) as i:
        megs = json.loads(i.read())
    i.close()
    return megs


def operate_sql(db, sql):
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    temp = cursor.fetchall()
    cursor.close()
    return temp


def pass_502(url):

    def headers():

        def union_id():
            def gen_id(length):
                chars = ['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
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

    response = requests.get(url=url, headers=headers())
    while re.search('502 Bad Gateway', response.content) is not None:
        time.sleep(0.2)
        response = requests.get(url=url, headers=headers())
    return response
