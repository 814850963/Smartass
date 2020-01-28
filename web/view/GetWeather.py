import datetime
import http
import json,time

import requests
from bs4 import BeautifulSoup
import urllib as urlparse

from web.models import *
ALL_DATA = []
def send_parse_urls():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        'Referer': 'http://www.weather.com.cn/weather1d/101070201.shtml',
    }
    url = 'http://d1.weather.com.cn/sk_2d/101070201.html?_='+str(int(round(time.time() * 1000)))
    response = requests.get(url,headers=headers)
    text = response.content.decode('utf-8')
    print(text)
    #str 转 json
    res = json.loads(text[text.index("{"):])
    date = datetime.date.today()
    temp = res['temp']
    intro = res['WD']+res['WS']+" "+res['weather']
    pm = res['aqi_pm25']
    t = time.time()
    Weather.objects.create(date=date,intro=intro,temp=temp,pm=pm,time=t)


send_parse_urls()
