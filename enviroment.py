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
2017.10.31
不知道print sql出现的IOError:[Error 0]是什么错误，只能先用异常处理语句将其避开
2017.11.1
1.发现向same服务器发送请求根本不需要构造header，删除
2.若出现ConnectionError，调用winsound库发出声音提醒更换IP
3.引起ConnectionError的原因可能是发送的数据包要求“keep-alive”，因此构造headers要求连接关闭
4.若出现ConnectionError，采用打开/关闭Shadowsocks.exe的方式解决，但某些时刻仍然出现此问题
"""
import json
import os
import time

import requests
import MySQLdb
import win32api
import winsound


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
    status = 1
    while status:
        try:
            response = requests.get(url=url)
        except requests.ConnectionError:
            y = os.system('taskkill /F /IM Shadowsocks.exe')
            winsound.Beep(233, 3000)
            time.sleep(7)
            if y:
                win32api.ShellExecute(0, 'open',
                                      u'C:\Application\Shadowsocks\备份\shadowsocks\Shadowsocks.exe'
                                      .encode('gbk'), '', '', 0)
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
            try:
                print sql
            except IOError:
                pass
        except IndexError:
            print "MySQL Error:%s" % str(e)
            print sql
