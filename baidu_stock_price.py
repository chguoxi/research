# -*- coding: utf-8 -*-  
import requests
import json
from dbconf import config
import time
import demjson
import pymysql
import sys
import os

base_url = 'https://gupiao.baidu.com/api/stocks/stockdaybar?from=pc&os_ver=1&cuid=xxx&vv=100&format=json&stock_code=hk%s&step=3&start=%s&count=600&fq_type=no&timestamp=%d'

t = time.time()
cdate = time.strftime('%Y%m%d')
#cdate = '20100101'
timestamp = int(round(t * 1000))
stock_file = './stock_list_hk.json'

conn=pymysql.connect(**config)
cur=conn.cursor()

s = requests.session()
s.keep_alive = False
requests.adapters.DEFAULT_RETRIES = 10

with open(stock_file) as fp:
    text = fp.read()
    stockdata = demjson.decode(text)
    try:
        for stock in stockdata:
            url = base_url % (stock['symbol'],cdate,timestamp)
            response = requests.get(url)
            # 抓取页面失败，重新尝试10次
            if int(response.status_code) != 200:
                sleep_time = 20
                for i in range(0,10):
                    print('''sleep %d second''' % sleep_time)
                    time.sleep(sleep_time)
                    response = requests.get(url)
                    if int(response.status_code) == 200:
                        break
                    else:
                        sleep_time = sleep_time + 30
                        continue
                
            if response.status_code !=200:
                sys.exit('can not crawl source url ')
            arr = demjson.decode(response.text)
            hisprice = arr['mashData']
            #print(hisprice[:4])
            #sys.exit()
            
            pricelist_len = len(hisprice)
            if pricelist_len > 0:
                sql = ''' INSERT INTO rsr_stock_price(`symbol`,`price`,`high`,`low`,`pre_close`,`amount`,`open`,`price_date`,`create_time`) values  '''
                for i in range(0,pricelist_len):
                    price= hisprice[i]['kline']
                    sql += ''' ('hk_%s',%f,%f,%f,%f,%d,%f,%s,NOW()) '''
                    sql = sql % (stock['symbol'],price['close'],price['high'],price['low'],price['preClose'],price['amount'],price['open'],hisprice[i]['date'])
                    if (i+1) % 600 ==0 or i== (pricelist_len-1):
                        sql += ''';'''
                        cur.execute(sql)
                        sql = ''' INSERT INTO rsr_stock_price(`symbol`,`price`,`high`,`low`,`pre_close`,`amount`,`open`,`price_date`,`create_time`) values  '''
                        
                    else:
                        sql += ''','''
            print('sleep 10 second...')
            time.sleep(10)
                    
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
    finally:
        fp.close()
        #print('-end--')
        #print(response.text)


    
