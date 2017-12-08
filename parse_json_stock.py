# -*- coding: utf-8 -*-
import json
import pymysql
import demjson
import os

stock_file = './stock_list_hk.json'

config = {
    'host': '45.56.91.103',
    'port': 3306,
    'user': 'stock_rsr',
    'passwd': '15336Hu89',
    'db': 'stock_rsr',
    'charset': 'utf8'
}

conn=pymysql.connect(**config)
cur=conn.cursor()

with open(stock_file) as fp:
    text = fp.read()
    jsondata = demjson.decode(text)
    sql = ''' INSERT INTO rsr_stock(`symbol`,`name`,`name_en`,`ipo_country`,`ipo_time`,`board`,`industry`) values (%s,%s,%s,'hk',null,'','') '''
    sql1 = ''' INSERT INTO rsr_stock_profile(`symbol`,`high_52week`,`low_52week`,`eps`,`prevclose`,`open`) values (%s,%s,%s,%s,%s,%s) '''
    for stock in jsondata:
        cur.execute(sql,('hk_'+stock['symbol'],stock['name'],stock['engname']))
        cur.execute(sql1,('hk_'+stock['symbol'],stock['high_52week'],stock['low_52week'],stock['eps'],stock['prevclose'],stock['open']))
        
    
