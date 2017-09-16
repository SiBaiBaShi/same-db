# _*_ coding: UTF-8 _*_
"""
2017.9.15
增加下载用户图片信息部分，但无法解析到用户数据，需要再分析应用数据包
2017.9.16
1.可以批量下载特定用户图片，保存路径为默认路径
2.条件语句输入时需自己输入sql结束符“;”
"""
from multiprocessing import Pool
import os

import MySQLdb

import enviroment


def download_by_user(user_list):
    for user_id in user_list:
        total_info = []
        url = 'https://v2.same.com/user/' + user_id + '/senses'
        response = enviroment.get_same_info(url)
        while 'next' in response.json()['data']:
            for text in response.json()['data']['results']:
                total_info.append([text['id'], text['channel_id'], text['photo']])
            next_url = 'https://v2.same.com' + response.json()['data']['next']
            response = enviroment.get_same_info(next_url)
        for text in response.json()['data']['results']:
            total_info.append([text['id'], text['channel_id'], text['photo']])
        name = response.json()['data']['results'][0]['user']['username'].encode('gbk', 'ignore')
        path = enviroment.USER_PATH + user_id + '-' + name + '\\'
        download(total_info, path)


def download_by_channel(c, w, p):
    """
    整理要下载的频道和保存路径信息
    :param c: 要下载的频道列表
    :param w: sql过滤语句
    :param p: 文件保存路径
    :return: None
    """
    channel_list = []
    path_list = []

    if c:
        for channel in c:
            channel_list.append(channel.decode('gbk'))
    else:
        channel_list = enviroment.CHANNEL

    if p:
        for path in p:
            path_list.append(path)
    else:
        for channel in channel_list:
            temp_w = w
            if '<' in w:
                temp_w = w.replace('<', 'smaller')
            if '>' in w:
                temp_w = w.replace('>', 'bigger')
            path_list.append(enviroment.PATH + temp_w + '\\' + channel.encode('gbk') + '\\')

    total_download_info = get_download_info(channel_list, w)

    for channel in channel_list:
        print "%-20s  %d" % (channel.encode('gbk'), len(total_download_info[channel]))

    for i, channel in enumerate(channel_list):
        download(total_download_info[channel], path_list[i])


def get_download_info(channel_list, where):
    total_download_info = {}
    db = MySQLdb.connect("59.110.136.121", "root", ">#hM%K4*", "same", charset='utf8')
    for i, channel in enumerate(channel_list):
        channel_id = enviroment.ID[channel]
        sql = 'select id, user_id, photo from {table_name} {where}' \
            .format(table_name='c' + str(channel_id),
                    where=where)
        total_download_info[channel] = enviroment.operate_sql(db, sql)
    return total_download_info


def download(download_info, path):
    is_exists = os.path.exists(path)
    if not is_exists:
        print 'build path = ' + path
        os.makedirs(path)

    pool = Pool(5)
    temp_path = path
    for image_info in download_info:
        path = r'{root_path}{id}same{user_id}.jpg'\
            .format(root_path=temp_path,
                    id=image_info[0],
                    user_id=image_info[1])
        pool.apply_async(enviroment.download_from_url, args=(image_info[2], path))
    pool.close()
    pool.join()
