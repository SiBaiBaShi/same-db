# _*_ coding: UTF-8 _*_
import os

import MySQLdb

import enviroment


def get_favor_list(path):
    """
    遍历目标文件夹内所有图片，然后调用
    :param path: 保存各频道favor图片文件夹的绝对路径
    :return:
    """
    # 得到需要更新的总数用于打印，便于显示进程
    total = now = 0
    for files in os.listdir(path):
        if os.path.isdir(path+'\\'+files):
            total += len(os.listdir(path+'\\'+files))

    db = MySQLdb.connect("59.110.136.121", "root", ">#hM%K4*", "same", charset='utf8')
    for files in os.listdir(path):
        if os.path.isdir(path+'\\'+files):
            for jpg in os.listdir(path+'\\'+files):
                write_favor(enviroment.ID[files.decode('gbk')],
                            jpg.split('same')[0] if 'same' in jpg else jpg.rstrip('.jpg'), db)
                now += 1
                print jpg, now, total
    db.close()


def write_favor(channel_id, image_id, db):
    """
    将channel_id的image_id的favor值改为1
    :param channel_id: 要修改favor值的表名
    :param image_id: 要修改favor值的图片id
    :param db: 用于使用cursor()执行sql命令
    :return:
    """
    sql = "update {table_name} set favor = 1 where id = {image_id};"\
        .format(table_name='c' + str(channel_id), image_id=image_id)
    enviroment.operate_sql(db, sql)
