# -*- coding: utf-8 -*-
import json
import pymysql

stock_file = './stock_list_hk.json'

config = {
    'host': '45.56.91.103',
    'port': 3306,
    'user': 'stock_rsr',
    'passwd': '15336Hu89',
    'db': 'stock_rsr',
    'charset': 'utf8'
}

jdata = json.loads(open(stock_file,'a'))

print(jdata)
try:
    conn=pymysql.connect(**config)
    cur=conn.cursor()
    #stocks = json.loads(open(stock_file,'a'))
    #sql = ''' INSERT INTO rsr_stock(`symbol`,`name`,`name_en`,`ipo_country`,`ipo_time`,`board`,`industry`) values ('%s','%s','%s','%s','%s','%s','%s') '''
    #for stock in stocks:
        #cur.execute(sql,(stock['name'],stock['engname'],'hk',null,null,null,null))
except Exception:
    print("Mysql Error")
    

