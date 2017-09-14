# _*_ coding: UTF-8 _*_
from multiprocessing import Pool
import os

import MySQLdb

import enviroment

root_path = r'C:\Users\root\Pictures\same\download\\'


def download_by_channel(c, w, p):
    # 获得频道信息
    info = enviroment.get_channel_info()
    names = info['names']
    ids = info['ids']
    channel_list = []
    path_list = []

    if c:
        for channel in c:
            channel_list.append(channel.decode('gbk'))
    else:
        channel_list = names
    if p:
        for path in p:
            path_list.append(path)
    else:
        for channel in channel_list:
            path_list.append(root_path + w + '\\' + channel.encode('gbk') + '\\')

    for i, channel in enumerate(channel_list):
        print channel.encode('gbk')
        table_name = 'channel' + ids[channel]
        prepare_for_download(table_name, w, path_list[i])


def prepare_for_download(table_name, where, path):
    is_exists = os.path.exists(path)
    if not is_exists:
        print 'build path = ' + path
        os.makedirs(path)

    db = MySQLdb.connect("59.110.136.121", "root", ">#hM%K4*", "same", charset='utf8')

    sql = 'select id, user_id, photo from {channel} where {where};' \
        .format(channel=table_name,
                where=where)
    result = enviroment.operate_sql(db, sql)

    pool = Pool(4)
    temp_path = path
    for image_info in result:
        path = r'{root_path}{id}same{user_id}.jpg'\
            .format(root_path=temp_path,
                    id=image_info[0],
                    user_id=image_info[1])
        pool.apply_async(enviroment.download_from_url, args=(image_info[2], path))
    pool.close()
    pool.join()

    db.close()
