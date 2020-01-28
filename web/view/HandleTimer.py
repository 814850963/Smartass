from django.http import JsonResponse
from django.views import View
import datetime
import json,time

import requests
from web.models import *

# 启动定时器
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

class WeatherControl(View):
    def get(self,request):
        flag = request.GET.get('flag')
        print(flag)
        print(type(flag))
        if flag == '1':
            #开启定时工作
            try:
                print(flag + "=================")
                # 实例化调度器
                scheduler = BackgroundScheduler()
                # 调度器使用DjangoJobStore()
                scheduler.add_jobstore(DjangoJobStore(), "default")
                # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
                @register_job(scheduler, 'cron', day_of_week='mon-sun', hour='0-23')
                def getWeather():
                    # headers = {
                    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
                    #     'Referer': 'http://www.weather.com.cn/weather1d/101070201.shtml',
                    # }
                    # url = 'http://d1.weather.com.cn/sk_2d/101070201.html?_=' + str(int(round(time.time() * 1000)))
                    # response = requests.get(url, headers=headers)
                    # text = response.content.decode('utf-8')
                    # print(text)
                    # # str 转 json
                    # res = json.loads(text[text.index("{"):])
                    # date = datetime.date.today()
                    # temp = res['temp']
                    # intro = res['WD'] + res['WS'] + " " + res['weather']
                    # pm = res['aqi_pm25']
                    # t = time.time()
                    # Weather.objects.create(date=date, intro=intro, temp=temp, pm=pm, time=t)
                    print(1)
                register_events(scheduler)
                scheduler.start()
            except Exception as e:
                print(e)
                # 有错误就停止定时器
                scheduler.shutdown()
            data = {
                "status": 1,
                "data":flag,
                "result": "修改成功",
            }
            return JsonResponse(data)
        else:
            scheduler = BackgroundScheduler()
            print(scheduler.get_jobs())
            data = {
                "status": 1,
                "data": flag,
                "result": "修改成功",
            }
            return JsonResponse(data)






