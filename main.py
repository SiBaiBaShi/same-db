# -*- coding: UTF-8 -*-
# 处理输入指令
"""
啊
"""
import argparse

import download
import favor
import index


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='python %(prog)s [options]',
                                     description=u'same应用图片下载\n'
                                                 u'无任何参数则下载前一周预设频道的图片\n'
                                                 u'默认均保存于\Saved Pictures\same\download\\'.encode('GBK'),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-a', nargs='*', default=[],
                        help=u'add,加入新的或更新预设频道信息；格式：“频道名 id 路径”'.encode('GBK'))
    parser.add_argument('-ad', nargs='?', const=False, default=True,
                        help=u'not add default,选择此选项则新频道不加入默认下载序列'.encode('GBK'))
    parser.add_argument('-s', nargs='?', const='all', default=False,
                        help=u'show,显示预设频道信息；无参数则显示全部，格式：“频道名”'.encode('GBK'))
    parser.add_argument('-d', nargs='*', default=[],
                        help=u'delete,删除频道预设信息；格式：“频道名(1) 频道名(2)”'.encode('GBK'))

    parser.add_argument('-b', nargs='*', default=[],
                        help=u'build,建立新的索引；格式：“频道名”'.encode('GBK'))
    parser.add_argument('-u', nargs='?', const='all', default=False,
                        help=u'update,更新索引；无参数则更新全部，格式：“频道名”'.encode('GBK'))

    parser.add_argument('-n', nargs='?', const=False, default=True,
                        help=u'not,若不下载图片，输入此提示符，无其它参数'.encode('GBK'))
    parser.add_argument('-c', nargs='*', default=[],
                        help=u'channel,频道名；可多个参数，格式：“频道名”'.encode('GBK'))
    parser.add_argument('-w', nargs='?', default=[],
                        help=u'time,时间范围；1或2个参数，格式：“Y-M-D H:M:S”'.encode('GBK'))
    parser.add_argument('-p', nargs='*', default=[],
                        help=u'path,保存路径；格式：“频道(1) 路径(1) 频道(2) 路径(2)”'.encode('GBK'))

    parser.add_argument('-f', nargs='?', default=False,
                        help=u'favor，更改favor值；格式：“（favor图片保存绝对路径）”'.encode('GBK'))
    args = parser.parse_args()

    if args.u:
        index.update(args.u)

    if args.n:
        download.download_by_channel(args.c, args.w, args.p)

    if args.f:
        favor.get_favor_list(args.f)
