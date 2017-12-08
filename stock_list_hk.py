# -*- coding: utf-8 -*-  
import requests
import json
import demjson

base_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHKStockData?page=%d&num=40&sort=symbol&asc=1&node=qbgg_hk&_s_r_a=page'
output_file = './stock_list_hk.json'

start_page = 1
end_page = 52

data = []

with open(output_file,'w') as f:  
    for page in range(start_page,end_page):
        #print(page)
        url = base_url % page
        response = requests.get(url)
        text = response.text.encode('utf-8')
        jdata = demjson.decode(text)
        for d in jdata:
            data.append(d)
    json.dump(data,f)

        
    



