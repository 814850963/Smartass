# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pymysql as pymysql
from django.shortcuts import render,HttpResponse,Http404

# Create your views here.

def test_view(request):
    print("执行了业务逻辑，安卓服务test没问题 ",request)
    print(dir(request))
    return HttpResponse("<h1 style='color:red'>成功します</h1>")

def login(request):
    # html = """
    #
    # """
    # return HttpResponse(html)
    #把html文件渲染
    return render(request,'form.html')

def ppp(request):
    return HttpResponse(request)

def  article(request):
    return HttpResponse('article 2003')

def article_archive(re,year):
    return HttpResponse('article archive %s'%year)
def sss(re,year):
    return HttpResponse('article year %s'%year)

def androidrequest(re,year):
    return HttpResponse('android in %s is running'%year)

def sql_test(re):
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='123456',db='smartassdatabase')
    cursor = conn.cursor() #游标
    cursor.execute("select * from a where name = 1")
    #取数据
    data = cursor.fetchall()
    return HttpResponse(data)