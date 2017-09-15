# _*_ coding: UTF-8 _*_
from multiprocessing import Pool
import os

import MySQLdb

import enviroment


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
        sql = 'select id, user_id, photo from {table_name} {where};' \
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
