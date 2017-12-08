# -*- coding: utf-8 -*-  
from rtstock.stock import Stock

stock = Stock('02357.hk')
prices = stock.get_latest_price()
print(prices)

        
    



