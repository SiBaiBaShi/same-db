# -*- coding: UTF-8 -*-
# 处理输入指令
import argparse

import download
import enviroment
import excel
import favor
import index


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='python %(prog)s [options]',
                                     description=u'same应用图片下载\n'
                                                 u'默认保存于C:\\Users\\root\Pictures\same\download\\'
                                     .encode('GBK'),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-dc', nargs='*', default=[],
                        help=u'download channel,频道名；'
                        .encode('GBK'))
    parser.add_argument('-dr', nargs='?', default='',
                        help=u'requirement，sql过滤条件；与sql条件语句完全一致'
                        .encode('GBK'))
    parser.add_argument('-dp', nargs='*', default=[],
                        help=u'path,保存路径；绝对路径，需有双引号'
                        .encode('GBK'))

    parser.add_argument('-es', nargs='?', default='',
                        help=u'excel sql，sql查询语句；与数据库环境完全一致'
                        .encode('GBK'))
    parser.add_argument('-ep', nargs='?', default='',
                        help=u'path，excel保存路径；绝对路径，需加上excel文件名和尾缀'
                        .encode('GBK'))

    parser.add_argument('-ud', nargs='?', const='all', default=False,
                        help=u'update database,更新数据库；无参数则更新所有频道'
                        .encode('GBK'))
    parser.add_argument('-uf', nargs='?', default=False,
                        help=u'favor，更改favor值；文件夹绝对路径，需有双引号'
                        .encode('GBK'))

    parser.add_argument('-sd', nargs='?', const='all', default=False,
                        help=u'show default,显示预设频道信息；无参数则显示所有频道'
                        .encode('GBK'))
    args = parser.parse_args()

    if args.dc:
        download.download_by_channel(args.dc, args.dr, args.dp)

    if args.es:
        excel.get_data(args.es, args.ep)

    if args.ud:
        index.update(args.ud)
    if args.uf:
        favor.get_favor_list(args.uf)

    if args.sd:
        enviroment.show(args.sd)
