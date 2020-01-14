import hashlib
import json
import os
from base64 import encode

from django.core import serializers
from django.views import View

from django.http import HttpResponse,JsonResponse
import cv2 as cv
from PIL import Image
from smartass import settings, Utils
from smartass.settings import BASE_DIR
from web.models import *

#获取课程列表
class ClassList(View):
    def get(self,request):
        page = request.GET.get('page')
        major = request.GET.get('major')
        course = request.GET.get('course')
        #条件搜索
        if major != None and page !=None and course!=None and course !='0' :
            classes = Class.objects.raw('select cc.*,c.name as cname,m.mname,c.majorid from major m inner join course c  on m.majorid='+major+' and c.majorid = '+major+' inner join class cc on cc.courseid = '+course+' and c.courseid = '+course)
            length = len(classes)
            temp = []
            for c in classes:
                temp.append(
                    {'classid': c.classid, 'name': c.name, 'mname': c.mname, 'coursename': c.cname, 'info': c.intro,'major': c.majorid,'status': c.status, 'course': c.courseid.courseid})
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[abs(int(page) - 1) * 10:abs(int(page) - 1) * 10 + 10],
                "page": abs(int(page)),
                "len": length
            }
            return JsonResponse(data)
        #带专业和课程查询
        elif page == None and major != None and course!=None and course !='0':
            classes = Class.objects.raw(
                'select cc.*,c.name as cname,m.mname,c.majorid from major m inner join course c  on m.majorid=' + major + ' and c.majorid = ' + major + ' inner join class cc on cc.courseid = ' + course + ' and c.courseid = ' + course)
            length = len(classes)
            temp = []
            for c in classes:
                temp.append(
                    {'classid': c.classid, 'name': c.name, 'mname': c.mname, 'coursename': c.cname, 'info': c.intro,
                     'major': c.majorid,'status': c.status, 'course': c.courseid.courseid})
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[0:10],
                "page": 1,
                "len": length
            }
            return JsonResponse(data)
        #专业搜索
        elif page==None and course=='0' and major!=None:
            classes = Class.objects.raw(
                'select cc.*,c.name as cname,m.mname,c.majorid from major m inner join course c  on m.majorid=' + major + ' and c.majorid = ' + major + ' inner join class cc on cc.courseid = c.courseid ')
            length = len(classes)
            temp = []
            for c in classes:
                temp.append(
                    {'classid': c.classid, 'name': c.name, 'mname': c.mname,'coursename':c.cname, 'info': c.intro, 'major': c.majorid,
                     'status': c.status, 'course': c.courseid.courseid})
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[0:10],
                "page": 1,
                "len": length
            }
            return JsonResponse(data)
        # 专业搜索
        elif page != None and course == '0' and major != None:
            classes = Class.objects.raw(
                'select cc.*,c.name as cname,m.mname,c.majorid from major m inner join course c  on m.majorid=' + major + ' and c.majorid = ' + major + ' inner join class cc on cc.courseid = c.courseid ')
            length = len(classes)
            temp = []
            for c in classes:
                temp.append(
                    {'classid': c.classid, 'name': c.name, 'mname': c.mname, 'coursename': c.cname, 'info': c.intro,
                     'major': c.majorid,
                     'status': c.status, 'course': c.courseid.courseid})
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[abs(int(page) - 1) * 10:abs(int(page) - 1) * 10 + 10],
                "page": 1,
                "len": length
            }
            return JsonResponse(data)
        # 普通搜索
        else:
            classes = Class.objects.raw(
                'select cc.*,c.name as cname,m.mname,c.majorid from major m inner join course c  on m.majorid= c.majorid inner join class cc on cc.courseid = c.courseid')
            length = len(classes)
            temp = []
            for c in classes:
                temp.append(
                    {'classid': c.classid, 'name': c.name, 'mname': c.mname, 'coursename': c.cname, 'info': c.intro,
                     'major': c.majorid,
                     'status': c.status, 'course': c.courseid.courseid})
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[0:10],
                "page": 1,
                "len": length
            }
            return JsonResponse(data)

#添加班级
class AddClass(View):
    def post(self,request):
        name = request.POST.get('name')
        info = request.POST.get('info')
        course = request.POST.get('course')
        course = Course.objects.get(courseid=course)
        # 插入数据
        if Class.objects.create(name=name, courseid=course,status=1,intro=info):
            data = {
                "status": 1,
                "result": "添加成功",
            }
            return JsonResponse(data)
        else:
            data = {
                "status": 0,
                "result": "添加失败",
            }
            return JsonResponse(data)


#修改课程
class ChangeClass(View):
    def post(self,request):
        name = request.POST.get('name')
        info = request.POST.get('info')
        course = request.POST.get('course')
        clasid = request.POST.get('clasid')
        print(clasid)
        if Class.objects.filter(classid=clasid).update(name=name,intro=info,courseid=course):
            data = {
                "status": 1,
                "result": "修改成功",
            }
            return JsonResponse(data)
        else:
            data = {
                "status": 0,
                "result": "修改失败",
            }
            return JsonResponse(data)


#修改课程状态
class ChangeClStatus(View):
    def post(self,request):
        pass

#获取专业以及课程信息
class GetAllMajorCourse(View):
    def get(self, request):
        majors = Major.objects.all().order_by('majorid').values()
        data = []
        children = []
        for i in majors:
            course = Course.objects.filter(majorid=i.get('majorid'))
            print(course)
            for c in course:
                children.append({
                    'value':c.courseid,
                    'label':c.name,
                })
            children.append({
                'value':0,
                'label':'当前专业'
            })
            instdata = {
                'value': i.get('majorid'),
                'label': i.get('mname'),
                'children': children}
            children = []
            data.append(instdata)
        instdata = {
            'value': 0,
            'label': '所有专业',}
        data.append(instdata)
        return JsonResponse(data,safe=False)