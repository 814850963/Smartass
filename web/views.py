# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import json

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render

# Create your views here.

# render(request,'form.html') 返回网页
from web.models import *



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