# -*- coding: UTF-8 -*-
# 处理输入指令
import argparse

import download
import enviroment
import favor
import index


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='python %(prog)s [options]',
                                     description=u'same应用图片下载\n'
                                                 u'默认保存于C:\\Users\\root\Pictures\same\download\\'
                                     .encode('GBK'),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-s', nargs='?', const='all', default=False,
                        help=u'show,显示预设频道信息；无参数则显示全部，格式：“频道名”'
                        .encode('GBK'))

    parser.add_argument('-u', nargs='?', const='all', default=False,
                        help=u'update,更新索引；无参数则更新全部，格式：“频道名”'.encode('GBK'))

    parser.add_argument('-n', nargs='?', const=False, default=True,
                        help=u'not,若不下载图片，输入此提示符即可'.encode('GBK'))
    parser.add_argument('-c', nargs='*', default=[],
                        help=u'channel,频道名；可多个参数，格式：“频道名”'.encode('GBK'))
    parser.add_argument('-w', nargs='?', default='',
                        help=u'where，sql过滤条件；如：where id=1 and views>100'.encode('GBK'))
    parser.add_argument('-p', nargs='*', default=[],
                        help=u'path,保存路径；绝对路径，需有双引号'
                        .encode('GBK'))

    parser.add_argument('-f', nargs='?', default=False,
                        help=u'favor，更改favor值；格式：“（favor图片保存绝对路径）”'
                        .encode('GBK'))
    args = parser.parse_args()

    if args.s:
        enviroment.show(args.s)

    if args.u:
        index.update(args.u)

    if args.n:
        download.download_by_channel(args.c, args.w, args.p)

    if args.f:
        favor.get_favor_list(args.f)
