# -*- coding: utf-8 -*-

import requests
import json
from dbconf import config
import time
import demjson
import pymysql
import sys
import os

class BaiduStock:
   
    price_base_url = 'https://gupiao.baidu.com/api/stocks/stockdaybar?from=pc&os_ver=1&cuid=xxx&vv=100&format=json&stock_code=hk%s&step=3&start=%s&count=%d&fq_type=no&timestamp=%d'
    ctime = ''
    dbcur = None
    price_count = 600
    stock_list_file = './stock_list_hk.json'
    logfile = './runtime.log'
    req = None
    
    def __init__(self):
        self.ctime = time.time()
        #print(config)
        self.conn(**config)
        requests.adapters.DEFAULT_RETRIES = 5
        self.req = requests.session()
        self.req.keep_alive = False
        
    def get_price_url(self,symbol):
        start = time.strftime('%Y%m%d')
        timestamp = int(round(self.ctime * 1000))
        price_url = self.price_base_url % (symbol,start,self.price_count,timestamp)
        return price_url
        
    def conn(self,**config):
        conn=pymysql.connect(**config)
        self.dbcur = conn.cursor()
        
    def get_price_list(self,symbol):

        url = self.get_price_url(symbol)
        resp = self.req.get(url,verify=False)
        if int(resp.status_code) == 200:
            arr = demjson.decode(resp.text)
            price_list = arr['mashData']
            return price_list
        else:
            return False

    def unexpect_interrupt(self,symbol):
        with open(self.logfile,'w+') as f:
            f.write(symbol)
            f.close()

    def save_price(self,symbol,pricelist):
        price_len = len(pricelist)
        init_sql = sql = '''INSERT INTO rsr_stock_price(`symbol`,`price`,`high`,`low`,`pre_close`,`amount`,`open`,`price_date`,`create_time`) values '''
        for i in range(0,price_len):
            price= pricelist[i]['kline']
            sql += ''' ('hk_%s',%f,%f,%f,%f,%d,%f,%s,NOW()) '''
            sql = sql % (symbol,price['close'],price['high'],price['low'],price['preClose'],price['amount'],price['open'],pricelist[i]['date'])
           
            if (i+1) % 600 ==0 or i== (price_len-1):
                sql += ''';'''
                self.dbcur.execute(sql)
                # 重新赋值
                sql = init_sql
                #self.dbcur.close()
            else:
                sql += ''','''

    def get_last_interrupt(self):
        with open(self.logfile,'a+') as f:
            symbol = f.read()
        return symbol

    def get_stock_list(self):
        with open(self.stock_list_file) as fp:
            text = fp.read()
            stockdata = demjson.decode(text)
            fp.close()
            return stockdata
    
    def price(self):
        last_interupt = self.get_last_interrupt()
        stockdata = self.get_stock_list()
        
        if last_interupt != '':
            stlen = len(stockdata)
            interupt_inde = 0
            for i in range(0,stlen):
                stock = stockdata[i]
                if stock['symbol'] == last_interupt :
                    interupt_inde = i;
                    break
            stocks = stockdata[interupt_inde:]
        else:
            stocks = stockdata
        #stocks = stocks[:2]
        stocks_len = len(stocks)
        #print(stocks_len)
        for idx in range(0,stocks_len):
            stock = stocks[idx]
            try:
                # 自动休眠
                pricelist = self.get_price_list(stock['symbol'])
                sleep_time = 10
                if pricelist is False:
                    for i in range(1,3):
                        print('''休眠%d秒...''' % sleep_time)
                        time.sleep(sleep_time)                                               
                        pricelist = self.get_price_list(stock['symbol'])
                        if pricelist is False:
                            sleep_time = 10
                            break
                        else:
                            sleep_time += 60
                            continue
                #print(pricelist)
                #sys.exit()
                if pricelist is False:
                    self.unexpect_interrupt(stock['symbol'])
                    print('request price failed ...')
                    sys.exit(0)                    
                elif len(pricelist)==0:
                    continue
                    
                self.save_price(stock['symbol'],pricelist)
                print('''休眠%d秒...''' % sleep_time)
                time.sleep(sleep_time)
            except Exception as err:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(err)
            finally:
                self.unexpect_interrupt(stock['symbol'])
            

bds = BaiduStock()
bds.price()
            
