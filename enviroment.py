# -*- coding: UTF-8 -*-
import random
import re
import time

import requests


CHANNEL = [u'我这么美我不能死', u'长腿A杯', u'轻性感', u'你觉得好看的samers',
           u'秀出你的身材', u'S.T.S.B.H.Q', u'DALUK', u'femininity']
DB_INFO = {
    'host': "59.110.136.121",
    'user': "root",
    'password': ">#hM%K4*",
    'database': "same",
    'charset': "utf8"
}
ID = {
    u'我这么美我不能死': 1015326,
    u'长腿A杯': 1032823,
    u'轻性感': 1033563,
    u'你觉得好看的samers': 1097342,
    u'秀出你的身材': 1112266,
    u'S.T.S.B.H.Q': 1125933,
    u'DALUK': 1166214,
    u'femininity': 1388511
}
PATH = r'C:\Users\root\Pictures\same\download\\'
URL = {
    u'我这么美我不能死': "https://v2.same.com/channel/1015326/senses",
    u'长腿A杯': "https://v2.same.com/channel/1032823/senses",
    u'轻性感': "https://v2.same.com/channel/1033563/senses",
    u'你觉得好看的samers': "https://v2.same.com/channel/1097342/senses",
    u'秀出你的身材': "https://v2.same.com/channel/1112266/senses",
    u'S.T.S.B.H.Q': "https://v2.same.com/channel/1125933/senses",
    u'DALUK': "https://v2.same.com/channel/1166214/senses",
    u'femininity': "https://v2.same.com/channel/1388511/senses"
}


def download_from_url(url, path):
    image = requests.get(url)
    with open(path, 'wb') as f:
        f.write(image.content)


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

    response = requests.get(url=url, headers=headers())
    while re.search('502 Bad Gateway', response.content) is not None:
        time.sleep(0.2)
        response = requests.get(url=url, headers=headers())
    return response


def operate_sql(db, sql):
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    temp = cursor.fetchall()
    cursor.close()
    return temp


def show(channel_name):
    if channel_name is 'all':
        for channel in CHANNEL:
            print "%-20s  %s" % (channel.encode('gbk'),  URL[channel])
    else:
        print channel_name, URL[channel_name.decode('gbk')]
