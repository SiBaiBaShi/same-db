# -*- coding: UTF-8 -*-
"""
2017.9.16
增加下载特定用户图片功能，命令行提示符为“-du”，可批量下载，图片保存路径固定为environment.USER_PATH
2017.9.19
增加预设频道信息的增删改查功能
"""
import argparse

import download
import excel
import favor
import index
import info


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='python %(prog)s [options]',
                                     description=u'same应用图片下载\n'
                                     .encode('GBK'),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-dc', nargs='*', default=[],
                        help=u'download channel,频道名；'
                        .encode('GBK'))
    parser.add_argument('-dr', nargs='?', default='',
                        help=u'requirement，sql过滤条件；与sql条件语句完全一致'
                        .encode('GBK'))
    parser.add_argument('-du', nargs='*', default=[],
                        help=u'user，用户id'
                        .encode('GBK'))
    parser.add_argument('-dp', nargs='*', default=[],
                        help=u'path,保存路径；绝对路径，需有双引号，用户图片有默认路径'
                        .encode('GBK'))

    parser.add_argument('-es', nargs='?', default='',
                        help=u'excel sql，sql查询语句；与数据库环境完全一致'
                        .encode('GBK'))
    parser.add_argument('-ep', nargs='?', default='',
                        help=u'path，excel保存路径；绝对路径，需加上excel文件名和尾缀'
                        .encode('GBK'))

    parser.add_argument('-bd', nargs='?', default=False,
                        help=u'build database,建立数据库'
                        .encode('GBK'))
    parser.add_argument('-ud', nargs='?', const='all', default=False,
                        help=u'update database,更新数据库；无参数则更新所有频道'
                        .encode('GBK'))
    parser.add_argument('-uf', nargs='?', default=False,
                        help=u'favor，更改favor值；文件夹绝对路径，需有双引号'
                        .encode('GBK'))

    parser.add_argument('-si', nargs='?', const='all', default=False,
                        help=u'show info,显示预设频道信息；无参数则显示所有频道'
                        .encode('GBK'))
    parser.add_argument('-ai', nargs='?', default=False,
                        help=u'add,添加预设频道信息；输入频道id'
                        .encode('GBK'))
    parser.add_argument('-di', nargs='?', default=False,
                        help=u'delete,删除预设频道信息；输入频道名'
                        .encode('GBK'))
    parser.add_argument('-mi', nargs='*', default=False,
                        help=u'modify,修改预设路径信息；预设信息 新路径'
                        .encode('GBK'))
    args = parser.parse_args()

    if args.dc:
        download.download_by_channel(args.dc, args.dr, args.dp)
    if args.du:
        download.download_by_user(args.du)

    if args.es:
        excel.get_data(args.es, args.ep)

    if args.bd:
        index.build(args.bd)
    if args.ud:
        index.update(args.ud)
    if args.uf:
        favor.get_favor_list(args.uf)

    if args.si:
        info.show(args.si)
    if args.ai:
        info.add(args.ai)
    if args.di:
        info.delete(args.di)
    if args.mi:
        info.modify(args.mi)
