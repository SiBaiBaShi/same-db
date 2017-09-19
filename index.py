# coding:utf-8"""2017.9.15增加向一个新表写入一个频道完整数据功能2017.9.17尝试多进程执行数据库命令，编写many_process函数将femininity频道580张图片的用户信息录入user库，多进程用时42.443秒，顺序执行用时49.495秒，平均每张节省0.012秒，5000张节省1分钟意义不大，暂不用2017.9.181.修改新建表逻辑，只有有图片的信息才能写入表2.增加user_end_id变量，并修改了inset_data(),其值等于更新前最新的图片id，因为用户信息较为稳定，    不必频繁更改，此id后的用户信息将不会写入用户表3.因日常使用需求，考虑更新截至id比任何图片都小的情况4.可以写入每张图片附带的txt信息5.可以录入用户的中文名2017.9.19新建表不再需要提前在数据库端操作"""from multiprocessing import Poolimport timeimport MySQLdbimport enviromentdef build(channel_id):    table_name = 'c' + str(channel_id)    url = "https://v2.same.com/channel/" + str(channel_id) + "/senses"    db = MySQLdb.connect(enviroment.DB_INFO['host'],                         enviroment.DB_INFO['user'],                         enviroment.DB_INFO['password'],                         enviroment.DB_INFO['database'],                         charset=enviroment.DB_INFO['charset'])    local_time = time.localtime(time.time())    few_days_ago = time.mktime([local_time.tm_year, local_time.tm_mon,                               local_time.tm_mday-3, 0, 0, 0, 0, 0, 0])    try:        mark = True        response = enviroment.get_same_info(url)        while 'next' in response.json()['data']:            for text in response.json()['data']['results']:                if text['photo']:                    insert_data(text, db, table_name, True)                    if mark:                        if text['created_at'] < few_days_ago:                            mark = False                            sql = "update channel_mark_id set id = {id} " \                                  "where channel = {d}{channel_name}{d};" \                                .format(id=text['id'],                                        channel_name=table_name,                                        d='\'')                            enviroment.operate_sql(db, sql)            url = 'https://v2.same.com' + response.json()['data']['next']            response = enviroment.get_same_info(url)        for text in response.json()['data']['results']:            insert_data(text, db, table_name)    finally:        db.close()def update(channel_list):    total = 0         # 总更新数    channel_num = {}  # 各频道更新数    db = MySQLdb.connect("59.110.136.121", "root", ">#hM%K4*", "same", charset='utf8')    # 设今日是A号，设A-4号的最后一张图片的ID为更新终止ID    local_time = time.localtime(time.time())    few_days_ago = time.mktime([local_time.tm_year, local_time.tm_mon,                               local_time.tm_mday-3, 0, 0, 0, 0, 0, 0])    if channel_list == 'all':        channel_list = enviroment.CHANNEL    else:        channel_list = [channel_list.decode('gbk')]    # update_info_list = []    for channel in channel_list:        num = 0        print channel.encode('gbk')        channel_id = enviroment.ID[channel]        table_name = 'c' + str(channel_id)        sql = 'select id from channel_mark_id where channel = {d}{channel_name}{d};'\            .format(channel_name=table_name,                    d='\'')        end_id = enviroment.operate_sql(db, sql)[0][0]        sql = 'select id from {table_name} order by id desc limit 1;'\            .format(table_name=table_name)        user_end_id = enviroment.operate_sql(db, sql)[0][0]        finish = 1   # 标记是否抵达终止ID        mark = True  # 标记是否可以更新数据库中的终止ID；更新一次后其值变为否        url = enviroment.URL[channel]        response = enviroment.get_same_info(url)        results = response.json()['data']['results']        while finish:            for text in results:                if text['id'] <= end_id:                    finish = 0                    break                else:                    if text['photo']:                        if text['id'] <= user_end_id:                            insert_data(text, db, table_name)                        else:                            insert_data(text, db, table_name, True)                        total += 1                        num += 1                    if mark:                        if text['created_at'] < few_days_ago:                            mark = False                            sql = "update channel_mark_id set id = {id} " \                                  "where channel = {d}{channel_name}{d};"\                                .format(id=text['id'],                                        channel_name='c' + str(channel_id),                                        d='\'')                            enviroment.operate_sql(db, sql)            if finish:                if 'next' not in response.json()['data']:                    finish = 0                else:                    next_url = 'https://v2.same.com' + response.json()['data']['next']                    response = enviroment.get_same_info(next_url)                    results = response.json()['data']['results']        channel_num[channel] = num    db.close()    # many_process(update_info_list)    for channel in channel_list:        print channel.encode('gbk'), channel_num[channel]    print '\ntotal update:', totaldef many_process(update_info_list):    # 若用多进程，须在insert_data函数内创建数据库连接    pool = Pool(4)    for info in update_info_list:        pool.apply_async(insert_data, args=(info[0], info[1]))    pool.close()    pool.join()def insert_data(photo, db, table_name, user_end=False):    photo['txt'] = photo['txt'].encode('utf-8', 'ignore')    if '\"' in photo['txt']:        photo['txt'] = photo['txt'].replace('\"', '“')    elif not photo['txt']:        photo['txt'] = 'null'    channel_command = \        "replace into {table_name} " \        "(id, user_id, time, likes, views, sex, photo, created_at, txt) " \        "values " \        "({id}, {user_id}, FROM_UNIXTIME({time}), {likes}, " \        "{views}, {sex}, {d}{photo}{d}, {created_at}, {d}{txt}{d});".\        format(            table_name=table_name,            id=photo['id'], user_id=photo['user']['id'],            time=photo['created_at'], photo=photo['photo'],            likes=photo['likes'], views=photo['views'],            sex=photo['user']['sex'], created_at=photo['created_at'],            txt=photo['txt'], d='\"')    if user_end:        user_info = photo['user']        user_command = \            "replace into user" \            "(user_id, user_name, time, created_at, " \            "sex, city_id, latest_area_change_at, timezone, " \            "password_set, firstblood) " \            "values " \            "({user_id}, {d}{user_name}{d}, FROM_UNIXTIME({time}), {created_at}, " \            "{sex}, {city_id}, {d}{latest_area_change_at}{d}, {d}{timezone}{d}, " \            "{d}{password_set}{d}, {firstblood});". \            format(                user_id=user_info['id'],                user_name=user_info['username'].encode('utf-8', 'ignore'),                time=user_info['created_at'],                created_at=user_info['created_at'],                sex=user_info['sex'],                city_id=user_info['meta']['city_id'] if 'city_id' in user_info['meta'] else -1,                latest_area_change_at=user_info['meta']['latest_area_change_at']                if 'latest_area_change_at' in user_info['meta'] else 0,                timezone=user_info['timezone'],                is_active=user_info['is_active'],                firstblood=user_info['meta']['firstblood'],                password_set=user_info['meta']['password_set'],                d='\"')        enviroment.operate_sql(db, user_command)    enviroment.operate_sql(db, channel_command)    print photo['id']