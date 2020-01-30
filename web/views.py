# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import json

from apscheduler.schedulers.blocking import BlockingScheduler
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render

# Create your views here.

# render(request,'form.html') 返回网页
from web.models import *

#启动定时器
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import datetime
import json,time

import requests
from web.models import *

#开启定时工作
try:
    # 实例化调度器
    weatherscheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    weatherscheduler.add_jobstore(DjangoJobStore(), "default")
    # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
    # @register_job(scheduler, 'cron', day_of_week='mon-sun', hour='0-23')
    @register_job(weatherscheduler, 'interval', hours=1)
    def job():
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            'Referer': 'http://www.weather.com.cn/weather1d/101070201.shtml',
        }
        url = 'http://d1.weather.com.cn/sk_2d/101070201.html?_=' + str(int(round(time.time() * 1000)))
        response = requests.get(url, headers=headers)
        text = response.content.decode('utf-8')
        print(text)
        # str 转 json
        res = json.loads(text[text.index("{"):])
        date = datetime.date.today()
        temp = res['temp']
        intro = res['WD'] + res['WS'] + " " + res['weather']
        pm = res['aqi_pm25']
        t = time.time()
        Weather.objects.create(date=date, intro=intro, temp=temp, pm=pm, time=t)
    register_events(weatherscheduler)
    weatherscheduler.start()

    # sched = BackgroundScheduler()
    #
    #
    # def my_job():
    #     print(f' Hello World ')
    #
    #
    # sched.add_job(my_job, 'interval', seconds=1)
    # sched.add_job(my_job, 'interval', seconds=2)
    # sched.add_job(my_job, 'interval', seconds=3)
    # sched.add_job(my_job, 'interval', seconds=4)
    # sched.add_job(my_job, 'interval', seconds=5)
    # sched.add_job(my_job, 'interval', seconds=6)
    # sched.add_job(my_job, 'interval', seconds=7)
    # sched.add_job(my_job, 'interval', seconds=8)
    # # 每5秒执行一次
    # sched.add_job(my_job, 'cron', hour='20', minute='30', second='00')
    # # 每天的20:30:00执行一次
    # sched.start()
except Exception as e:
    print(e)
    # 有错误就停止定时器
    weatherscheduler.shutdown()

def login(request):
    md5 = hashlib.md5()
    md5.update(request.POST.get('passwd').encode("utf-8"))
    result = md5.hexdigest()
    print(result)
    admin = Admin.objects.filter(name=request.POST.get('name'),passwd=result)
    print(admin[0])
    print(admin[0].adminid)
    if admin:
        data = {
            "status": 1,
            "result": "登录成功",
            "authen": admin[0].adminid
        }
    else:
        data = {
            "status": 0,
            "result": "账号密码不正确"
        }

    return JsonResponse(data)
    # return HttpResponse(json.dumps(da), content_type="application/json")