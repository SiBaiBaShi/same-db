# coding:utf-8"""2017.9.15增加向一个新表写入一个频道完整数据功能2017.9.17尝试多进程执行数据库命令，编写many_process函数将femininity频道580张图片的用户信息录入user库，多进程用时42.443秒，顺序执行用时49.495秒，平均每张节省0.012秒，5000张节省1分钟意义不大，暂不用2017.9.181.修改新建表逻辑，只有有图片的信息才能写入表2.增加user_end_id变量，并修改了inset_data(),其值等于更新前最新的图片id，因为用户信息较为稳定，    不必频繁更改，此id后的用户信息将不会写入用户表3.因日常使用需求，考虑更新截至id比任何图片都小的情况4.可以写入每张图片附带的txt信息5.可以录入用户名2017.9.191.新建表不再需要提前在数据库端操作2.将预设信息保存在info.json文件中，而不是python程序内2017.10.23更新图片增加对无法访问图片的处理2017.10.301.更新频道内容时，增加对新图片的计数2.优化了判定更新哪些图片的代码2017.10.311.增加了下载并更新重要用户最新图片的函数update_user_value()2.修复了打印更新的图片id时出现的IOError"""import timefrom MySQLdb import connectimport enviromentfrom download import downloadfrom info import changedef build(channel_id):    db = connect(enviroment.get_info('DB_INFO')['host'],                 enviroment.get_info('DB_INFO')['user'],                 enviroment.get_info('DB_INFO')['password'],                 enviroment.get_info('DB_INFO')['database'],                 charset=enviroment.get_info('DB_INFO')['charset'])    build_info(channel_id)    table_name = 'c' + str(channel_id)    url = "https://v2.same.com/channel/" + str(channel_id) + "/senses"    local_time = time.localtime(time.time())    update_time = time.mktime([local_time.tm_year, local_time.tm_mon,                               local_time.tm_mday-3, 0, 0, 0, 0, 0, 0])    mark = True    response = enviroment.get_same_info(url)    while 'next' in response.json()['data']:        for text in response.json()['data']['results']:            if text['photo']:                insert_data(text, db, table_name, True)                if mark:                    if text['created_at'] < update_time:                        mark = False                        sql = "update channel_mark_id set id = {id} " \                              "where channel = {d}{channel_name}{d};" \                            .format(id=text['id'],                                    channel_name=table_name,                                    d='\'')                        enviroment.operate_sql(db, sql)        url = 'https://v2.same.com' + response.json()['data']['next']        response = enviroment.get_same_info(url)    for text in response.json()['data']['results']:        if text['photo']:            insert_data(text, db, table_name, True)    db.close()def build_info(channel_id):    db = connect(enviroment.get_info('DB_INFO')['host'],                 enviroment.get_info('DB_INFO')['user'],                 enviroment.get_info('DB_INFO')['password'],                 enviroment.get_info('DB_INFO')['database'],                 charset=enviroment.get_info('DB_INFO')['charset'])    sql = "create table {table_name} like channel;"\        .format(table_name='c'+channel_id)    enviroment.operate_sql(db, sql)    sql = "replace into channel_mark_id (channel, id) values ({d}{table_name}{d}, 0);"\        .format(table_name='c'+channel_id, d='\"')    enviroment.operate_sql(db, sql)def update(channel_list):    update_user = 0    total = 0         # 总更新数    total_new = 0    channel_num = {}  # 各频道更新数    new_num = {}    db = connect(enviroment.get_info('DB_INFO')['host'],                 enviroment.get_info('DB_INFO')['user'],                 enviroment.get_info('DB_INFO')['password'],                 enviroment.get_info('DB_INFO')['database'],                 charset=enviroment.get_info('DB_INFO')['charset'])    # 设今日是A号，设A-4号的最后一张图片的ID为更新终止ID    local_time = time.localtime(time.time())    update_time = time.mktime([local_time.tm_year, local_time.tm_mon,                               local_time.tm_mday-3, 0, 0, 0, 0, 0, 0])    if channel_list == 'all':        channel_list = sorted(enviroment.get_info('ID').keys(),                              key=lambda x: enviroment.get_info('ID')[x], reverse=True)        update_user = 1    else:        channel_list = [channel_list.decode('gbk')]    for channel in channel_list:        num = 0        new = 0        print '\n', channel.encode('gbk'), '\n'        channel_id = enviroment.get_info('ID')[channel]        table_name = 'c' + str(channel_id)        sql = 'select id from channel_mark_id where channel = {d}{channel_name}{d};'\            .format(channel_name=table_name,                    d='\'')        end_id = enviroment.operate_sql(db, sql)[0][0]        sql = 'select id from {table_name} order by id desc limit 1;'\            .format(table_name=table_name)        user_end_id = enviroment.operate_sql(db, sql)[0][0]        finish = 1   # 标记是否抵达终止ID        mark = True  # 标记是否可以更新数据库中的终止ID；更新一次后其值变为否        url = "https://v2.same.com/channel/" + str(enviroment.get_info('ID')[channel]) + "/senses"        response = enviroment.get_same_info(url)        try:            results = response.json()['data']['results']        except ValueError:            print response.content        except KeyError:            print u'此频道无法再访问'.encode('gbk')            channel_list.remove(channel)            change(channel)            break        else:            while finish:                for text in results:                    if text['id'] <= end_id:                        finish = 0                        break                    else:                        if text['photo'] and text['id'] <= user_end_id:                            insert_data(text, db, table_name)                        elif text['photo']:                            insert_data(text, db, table_name, True)                            new += 1                            total_new += 1                        total += 1                        num += 1                        if mark and text['created_at'] < update_time:                            mark = False                            sql = "update channel_mark_id set id = {id} " \                                  "where channel = {d}{channel_name}{d};"\                                .format(id=text['id'],                                        channel_name='c' + str(channel_id),                                        d='\'')                            enviroment.operate_sql(db, sql)                if finish:                    if 'next' not in response.json()['data']:                        finish = 0                    else:                        next_url = 'https://v2.same.com' + response.json()['data']['next']                        response = enviroment.get_same_info(next_url)                        results = response.json()['data']['results']        channel_num[channel] = num        new_num[channel] = new    db.close()    print '\n'    for channel in channel_list:        print "%-24s  %-4d  %-4d" % (channel.encode('gbk'), channel_num[channel], new_num[channel])    print '\ntotal update:', total    print '\ntotal new image:', total_new    if update_user:        update_user_value()def insert_data(photo, db, table_name, user_end=False):    photo['txt'] = photo['txt'].encode('utf-8', 'ignore')    if '\"' in photo['txt']:        photo['txt'] = photo['txt'].replace('\"', '“')    elif not photo['txt']:        photo['txt'] = ' '    channel_command = \        "replace into {table_name} " \        "(id, user_id, time, likes, views, sex, photo, created_at, txt) " \        "values " \        "({id}, {user_id}, FROM_UNIXTIME({time}), {likes}, " \        "{views}, {sex}, {d}{photo}{d}, {created_at}, {d}{txt}{d});".\        format(            table_name=table_name,            id=photo['id'], user_id=photo['user']['id'],            time=photo['created_at'], photo=photo['photo'],            likes=photo['likes'], views=photo['views'],            sex=photo['user']['sex'], created_at=photo['created_at'],            txt=photo['txt'], d='\"')    if user_end:        user_info = photo['user']        user_command = \            "replace into user" \            "(user_id, user_name, time, created_at, " \            "sex, city_id, latest_area_change_at, timezone, " \            "password_set, firstblood) " \            "values " \            "({user_id}, {d}{user_name}{d}, FROM_UNIXTIME({time}), {created_at}, " \            "{sex}, {city_id}, {d}{latest_area_change_at}{d}, {d}{timezone}{d}, " \            "{d}{password_set}{d}, {firstblood});". \            format(                user_id=user_info['id'],                user_name=user_info['username'].encode('utf-8', 'ignore'),                time=user_info['created_at'],                created_at=user_info['created_at'],                sex=user_info['sex'],                city_id=user_info['meta']['city_id'] if 'city_id' in user_info['meta'] else -1,                latest_area_change_at=user_info['meta']['latest_area_change_at']                if 'latest_area_change_at' in user_info['meta'] else 0,                timezone=user_info['timezone'],                is_active=user_info['is_active'],                firstblood=user_info['meta']['firstblood'],                password_set=user_info['meta']['password_set'],                d='\"')        enviroment.operate_sql(db, user_command)    try:        enviroment.operate_sql(db, channel_command)        print photo['id']    except IOError as e:        print edef update_user_value():    db = connect(enviroment.get_info('DB_INFO')['host'],                 enviroment.get_info('DB_INFO')['user'],                 enviroment.get_info('DB_INFO')['password'],                 enviroment.get_info('DB_INFO')['database'],                 charset=enviroment.get_info('DB_INFO')['charset'])    sql = "select user_id, image_id from user_value where live = 1;"    user_value = enviroment.operate_sql(db, sql)    for user_info in user_value:        finish = 1        total_info = []        url = 'https://v2.same.com/user/' + str(user_info[0]) + '/senses'        response = enviroment.get_same_info(url)        try:            results = response.json()['data']['results']            image_id = results[0]['id']            while finish:                for text in results:                    if text['id'] <= user_info[1]:                        finish = 0                        break                    elif text['photo'] and text['likes'] >= 20:                        total_info.append([text['id'], text['channel_id'], text['photo']])                if finish:                    if 'next' not in response.json()['data']:                        finish = 0                    else:                        next_url = 'https://v2.same.com' + response.json()['data']['next']                        response = enviroment.get_same_info(next_url)                        results = response.json()['data']['results']            name = response.json()['data']['results'][0]['user']['username']        except IndexError:            print '\n\n user_id = %d cancelled\n\n' % user_info[0]            sql = 'update user_value set live = 0 where user_id = {user_id};'\                .format(user_id=user_info[0])            enviroment.operate_sql(db, sql)        else:            path = enviroment.get_info('USER_PATH') + str(user_info[0]) + '-' + name + '\\'            if total_info:                download(total_info, path)            sql = 'update user_value set image_id = {image_id} where user_id = {user_id};'\                .format(image_id=image_id, user_id=user_info[0])            enviroment.operate_sql(db, sql)    db.close()