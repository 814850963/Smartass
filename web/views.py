# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import json

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render

# Create your views here.

# render(request,'form.html') 返回网页
from web.models import *
from web.view import  GetWeather

#启动定时器
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

#开启定时工作
try:
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
    @register_job(scheduler, 'cron', day_of_week='mon-sun', hour='0-23')
    def my_job():
        GetWeather.send_parse_urls()
    register_events(scheduler)
    scheduler.start()
except Exception as e:
    print(e)
    # 有错误就停止定时器
    scheduler.shutdown()

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