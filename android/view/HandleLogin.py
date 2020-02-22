import hashlib

from django.http import JsonResponse
from django.views import View

from android.models import *
from smartass import Utils, settings

import cv2
import os
import dlib
from skimage import io
import csv
import numpy as np

class Login(View):
    def post(self,request):
        account = request.POST.get('account')
        password = request.POST.get("password")
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        result = md5.hexdigest()
        student = Student.objects.filter(account=account, passwd=result,status=1)
        if student:
            data = {
                "status": 1,
                "result": "登录成功",
                "auth": student[0].studentid,
                "identity": 1
            }
        else:
            teacher = Teacher.objects.filter(account=account, passwd=result)
            if teacher:
                data = {
                    "status": 1,
                    "result": "登录成功",
                    "auth": teacher[0].teacherid,
                    "identity": 0
                }
            else:
                data = {
                    "status": 0,
                    "result": "账号密码不正确",
                    "auth": None
                }

        return JsonResponse(data)

#获取个人信息
class GetPersonProfile(View):
    def post(self,request):
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
        background = None
        if identity == '1':
            s = Student.objects.get(studentid=auth)
            if s.background != None:
                background = Utils.HOST + Utils.PENGYOU_URL + s.background
            data = {
                'name': s.name,
                'pic': Utils.HOST + Utils.PIC_URL +s.headpic,
                'background': background,
            }
        elif identity == '0':
            t = Teacher.objects.get(teacherid=auth)
            if t.background != None:
                background = Utils.HOST + Utils.PENGYOU_URL + t.background
            data = {
                'name': t.name,
                'pic': Utils.HOST + Utils.PIC_URL +t.pic,
                'image': background,
            }
        print(data)
        data = {
            "status": '1',
            "result": "成功",
            "data": data
        }
        return JsonResponse(data)
