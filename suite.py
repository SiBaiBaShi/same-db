# _*_ coding: UTF-8 _*_
import os
import shutil

import enviroment
import MySQLdb


def delete_empty_file(path):
    # 删除空文件夹，注意遍历层级
    for files in os.listdir(path):
        # if os.path.isdir(path+'\\'+files):
        if not os.listdir(path+'\\'+files):
            os.rmdir(path+'\\'+files)


def copy_to_root(path):
    # 将一个文件夹内的图片拷贝到另一个文件夹中，其实使用好os.listdir()和shutil.copy()函数即可
    for files in os.listdir(path):
        # if os.path.isdir(path+'\\'+files):
        for jpg in os.listdir(path+'\\'+files):
            shutil.copy(path+'\\'+files+'\\'+jpg, path+'\\'+jpg)


def delete_jpg(path):
    # 删除数据库和本地重复存在的图片，使用时注意程序遍历层级、sql查找条件以及图片名处理规则
    db = MySQLdb.connect("59.110.136.121", "root", ">#hM%K4*", "same", charset='utf8')
    sql = "select id from c1032823 where id > 68733400;"
    response = enviroment.operate_sql(db, sql)
    db.close()
    for files in os.listdir(path):
        # if os.path.isdir(path+'\\'+files):
        # for jpg in os.listdir(path+'\\'+files):
            for i, info in enumerate(response):
                if info[0] == int(files.split('same')[0]):
                    os.remove(path + '\\' + files)
                    print 'delete', files
                    response = response[i+1:]
                    break


def get_channel_info(channel_id):
    url = "https://v2.same.com/channel/" + str(channel_id) + "/senses"
    response = enviroment.get_same_info(url)
    results = response.json()['data']['results'][0]
    print "channel : %s" % results['channel']['name'].encode('utf-8', 'ignore')
    print "user_id : %d" % results['channel']['user_id']
    if 'next' in response.json()['data']:
        print 'channel has next'


if __name__ == '__main__':
    # delete_empty_file(unicode(r'C:\Users\root\Pictures\same\channel', 'utf-8').encode('gbk'))
    # copy_to_root(unicode(r'C:\Users\root\Pictures\same\no\轻性感\分时', 'utf-8').encode('gbk'))
    # delete_jpg(unicode(r'C:\Users\root\Pictures\same\channel\长腿A杯', 'utf-8').encode('gbk'))
    get_channel_info(1092473)
