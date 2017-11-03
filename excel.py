# _*_ coding: UTF-8 _*_
import xlwings as xw
from MySQLdb import connect

import enviroment


def get_data(sql, path):
    db = connect(enviroment.get_info('DB_INFO')['host'],
                 enviroment.get_info('DB_INFO')['user'],
                 enviroment.get_info('DB_INFO')['password'],
                 enviroment.get_info('DB_INFO')['database'],
                 charset=enviroment.get_info('DB_INFO')['charset'])
    data = enviroment.operate_sql(db, sql)
    print 'row : ', len(data), '   column :  ', len(data[0])

    columns = sql.lower().split('from')[0].lstrip('select').replace(' ', '').split(',')
    for i in range(len(columns)):
        if 'as' in columns[i]:
            columns[i] = columns[i].split('as')[1].lstrip('\"').rstrip('\"')

    input_excel(data, columns, path)


def input_excel(data, columns, path):
    wb = xw.Book()
    sheet = wb.sheets['sheet1']
    # 'A'=65
    i = 65
    for column in columns:
        sheet.range(chr(i)+'1').value = column
        i += 1

    j = 2
    for row in data:
        i = 65
        for block in row:
            sheet.range(chr(i) + str(j)).value = block
            i += 1
        j += 1

    wb.save(path)
    wb.close()
