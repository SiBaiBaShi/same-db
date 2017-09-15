# _*_ coding: UTF-8 _*_
import xlwings as xw
import MySQLdb

import enviroment


def get_data(sql, path):
    db = MySQLdb.connect(enviroment.DB_INFO['host'],
                         enviroment.DB_INFO['user'],
                         enviroment.DB_INFO['password'],
                         enviroment.DB_INFO['database'],
                         charset=enviroment.DB_INFO['charset'])
    data = enviroment.operate_sql(db, sql)
    print 'row : ', len(data), '   column :  ', len(data[0])

    columns = sql.split('from')[0].lstrip('select').replace(' ', '').split(',')

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
