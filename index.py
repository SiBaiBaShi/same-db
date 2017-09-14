# _*_ coding: unicode _*_
"""
2017.9.14
更新操作尚不能一键全部更新   2017.9.14已解决
"""
import time

import MySQLdb

import enviroment


def update(channel_list):
    db = MySQLdb.connect("59.110.136.121", "root", ">#hM%K4*", "same", charset='utf8')
    # 获得频道信息
    info = enviroment.get_channel_info()
    names = info['names']
    urls = info['urls']
    ids = info['ids']

    # 只更新三天前的信息
    local_time = time.localtime(time.time())
    two_day_ago = time.mktime([local_time.tm_year, local_time.tm_mon, local_time.tm_mday-2, 0, 0, 0, 0, 0, 0])

    # 要更新的频道，手动输入的频道信息要转码为unicode
    if channel_list == 'all':
        channel_list = names
    else:
        channel_list = [channel_list.decode('gbk')]

    for channel in channel_list:
        print channel.encode('gbk')
        channel_id = 'channel' + ids[channel]
        # 获取目标表的最近id为终止id
        sql = 'select id from {channel_id} order by id desc limit 1;'\
            .format(channel_id=channel_id)
        end_id = enviroment.operate_sql(db, sql)[0][0]

        finish = 1  # 标记为是否更新完成

        url = urls[ids[channel]]
        response = enviroment.pass_502(url)
        results = response.json()['data']['results']
        while finish:
            for text in results:
                # 当前id小于等于终止id时结束
                if text['id'] <= end_id:
                    finish = 0
                    break
                else:
                    if text['created_at'] < two_day_ago and text['photo']:
                        update_sql(text, db, channel_id)
            if finish:
                next_url = 'https://v2.same.com' + response.json()['data']['next']
                response = enviroment.pass_502(next_url)
                results = response.json()['data']['results']
    db.close()


def update_sql(photo, db, channel_id):
    channel_command = \
        "replace into " + channel_id + \
        "(id, user_id, time, likes, views, sex, photo, created_at) " \
        "values " \
        "({id},{user_id},FROM_UNIXTIME({time}),{likes},{views},{sex},{d}{photo}{d}, {created_at});".\
        format(
                    id=photo['id'], user_id=photo['user']['id'],
                    time=photo['created_at'], photo=photo['photo'],
                    likes=photo['likes'], views=photo['views'],
                    sex=photo['user']['sex'], created_at=photo['created_at'],
                    d='\"')

    user_info = photo['user']
    user_command = \
        "replace into user" \
        "(user_id, time, created_at, sex, city_id, " \
        "latest_area_change_at, timezone, password_set, firstblood) " \
        "values " \
        "({user_id}, FROM_UNIXTIME({time}), {created_at}, {sex}, {city_id}, " \
        "{d}{latest_area_change_at}{d}, {d}{timezone}{d}, {d}{password_set}{d}, {firstblood});". \
        format(
            user_id=user_info['id'],
            time=user_info['created_at'],
            created_at=user_info['created_at'],
            sex=user_info['sex'],
            city_id=user_info['meta']['city_id'] if 'city_id' in user_info['meta'] else -1,
            latest_area_change_at=user_info['meta']['latest_area_change_at']
            if 'latest_area_change_at' in user_info['meta'] else '0-0-0 0:0:0',
            timezone=user_info['timezone'],
            is_active=user_info['is_active'],
            firstblood=user_info['meta']['firstblood'],
            password_set=user_info['meta']['password_set'],
            d='\"')

    enviroment.operate_sql(db, channel_command)
    enviroment.operate_sql(db, user_command)

    print photo['id']
