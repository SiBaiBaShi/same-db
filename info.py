# -*- coding: UTF-8 -*-
# 用于增加、更新和删除频道信息
import json

import enviroment


def add(channel_id):
    url = "https://v2.same.com/channel/" + channel_id + "/senses"
    response = enviroment.get_same_info(url)
    channel_name = response.json()['data']['results'][0]['channel']['name']
    temp = channel_name.encode('utf-8', 'ignore')
    channel_name = temp.decode('utf-8')

    with open(enviroment.INFO) as f:
        info = json.loads(f.read())
    f.close()
    info['ID'][channel_name] = int(channel_id)
    info['CHANNEL'].append(channel_name)
    print channel_name.encode('gbk', 'ignore'), info['ID'][channel_name]

    with open(enviroment.INFO, 'w') as f:
        f.write(json.dumps(info))
    f.close()


def delete(channel_name):
    with open(enviroment.INFO) as f:
        info = json.loads(f.read())
    f.close()
    try:
        channel = channel_name.decode('GBK')  # 频道名
        if channel in info['CHANNEL']:
            info['CHANNEL'].remove(channel)
        if channel in info['ID']:
            info['ID'].pop(channel)
    except KeyError:
        print u'无此频道'.encode('gbk')
    else:
        with open(enviroment.INFO, 'w') as f:
            f.write(json.dumps(info))
        f.close()
        print u'已删除'.encode('gbk')


def modify(meg):
    with open(enviroment.INFO) as f:
        info = json.loads(f.read())
    f.close()
    try:
        if meg[0] in info:
            info[meg[0]] = meg[1].decode('utf-8')
            with open(enviroment.INFO, 'w') as f:
                f.write(json.dumps(info))
            f.close()
    except KeyError:
        print '无该变量'.encode('gbk')


def show(channel_name):
    with open(enviroment.INFO) as f:
        info = json.loads(f.read())
    f.close()
    if channel_name == 'all':
        print "%-24s  %s" % ('INFO', info['INFO'])
        print "%-24s  %s" % ('PATH', info['PATH'])
        print "%-24s  %s" % ('USER_PATH', info['USER_PATH'])
        print '\n'
        for name in info['ID'].items():
            print '\n', "%-24s  %d" % (name[0].encode('GBK'), info['ID'][name[0]])
    else:
        try:
            print channel_name + ' ' + str(info['ID'][channel_name.decode('gbk')])
        except KeyError:
            print u"无该频道".encode('gbk')
