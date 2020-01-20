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
            count = 0
            for c in classes:
                temp.append(
                    {'classid': c.classid, 'name': c.name, 'mname': c.mname, 'coursename': c.cname, 'info': c.intro,
                     'major': c.majorid, 'status': c.status, 'course': c.courseid.courseid, 'place': c.place,
                     'time': c.time, 'count': c.count,'teacherid':c.teacherid.teacherid,'weekday':c.weekday,'total':c.total})
                c = Class.objects.raw('select c.*,t.name as tname from class c inner join teacher t on c.teacherid = t.teacherid and c.classid= '+str(c.classid))
                c = c[0]
                temp[count]['tname'] = c.tname
                print(temp[count])
                count+=1
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[abs(int(page) - 1) * 10:abs(int(page) - 1) * 10 + 10],
                "page": abs(int(page)),
                "len": length
            }
            return JsonResponse(data)
        # 条件搜索
        elif major == None and int(page) >1 and course == None:
            classes = Class.objects.raw(
                'select cc.*,c.name as cname,m.mname,c.majorid from major m inner join course c  on m.majorid = c.majorid inner join class cc on cc.courseid = c.courseid ' )
            length = len(classes)
            temp = []
            count = 0
            for c in classes:
                temp.append(
                    {'classid': c.classid, 'name': c.name, 'mname': c.mname, 'coursename': c.cname, 'info': c.intro,
                     'major': c.majorid, 'status': c.status, 'course': c.courseid.courseid, 'place': c.place,
                     'time': c.time, 'count': c.count, 'teacherid': c.teacherid.teacherid, 'weekday': c.weekday,
                     'total': c.total})
                c = Class.objects.raw(
                    'select c.*,t.name as tname from class c inner join teacher t on c.teacherid = t.teacherid and c.classid= ' + str(
                        c.classid))
                c = c[0]
                temp[count]['tname'] = c.tname
                print(temp[count])
                count += 1
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
            count = 0
            for c in classes:
                temp.append(
                    {'classid': c.classid, 'name': c.name, 'mname': c.mname, 'coursename': c.cname, 'info': c.intro,
                     'major': c.majorid, 'status': c.status, 'course': c.courseid.courseid, 'place': c.place,
                     'time': c.time, 'count': c.count, 'teacherid': c.teacherid.teacherid,'weekday':c.weekday,'total':c.total})
                c = Class.objects.raw(
                    'select c.*,t.name as tname from class c inner join teacher t on c.teacherid = t.teacherid and c.classid= ' + str(
                        c.classid))
                c = c[0]
                temp[count]['tname'] = c.tname
                count += 1
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
            count = 0
            for c in classes:
                temp.append(
                    {'classid': c.classid, 'name': c.name, 'mname': c.mname, 'coursename': c.cname, 'info': c.intro,
                     'major': c.majorid, 'status': c.status, 'course': c.courseid.courseid, 'place': c.place,
                     'time': c.time, 'count': c.count, 'teacherid': c.teacherid.teacherid,'weekday':c.weekday,'total':c.total})
                c = Class.objects.raw(
                    'select c.*,t.name as tname from class c inner join teacher t on c.teacherid = t.teacherid and c.classid= ' + str(
                        c.classid))
                c = c[0]
                temp[count]['tname'] = c.tname
                count += 1
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
            count = 0
            for c in classes:
                temp.append(
                    {'classid': c.classid, 'name': c.name, 'mname': c.mname, 'coursename': c.cname, 'info': c.intro,
                     'major': c.majorid, 'status': c.status, 'course': c.courseid.courseid, 'place': c.place,
                     'time': c.time, 'count': c.count, 'teacherid': c.teacherid.teacherid,'weekday':c.weekday,'total':c.total})
                c = Class.objects.raw(
                    'select c.*,t.name as tname from class c inner join teacher t on c.teacherid = t.teacherid and c.classid= ' + str(
                        c.classid))
                c = c[0]
                temp[count]['tname'] = c.tname
                count += 1
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
            count = 0
            for c in classes:
                temp.append(
                    {'classid': c.classid, 'name': c.name, 'mname': c.mname, 'coursename': c.cname, 'info': c.intro,
                     'major': c.majorid, 'status': c.status, 'course': c.courseid.courseid, 'place': c.place,
                     'time': c.time, 'count': c.count, 'teacherid': c.teacherid.teacherid,'weekday':c.weekday,'total':c.total})
                c = Class.objects.raw(
                    'select c.*,t.name as tname from class c inner join teacher t on c.teacherid = t.teacherid and c.classid= ' + str(
                        c.classid))
                c = c[0]
                temp[count]['tname'] = c.tname
                count += 1
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
        place = request.POST.get('place')
        time = request.POST.get('time')
        count = request.POST.get('count')
        course = request.POST.get('course')
        teacherid = request.POST.get('teacherid')
        t = Teacher.objects.get(teacherid=teacherid)
        course = Course.objects.get(courseid=course)
        total = request.POST.get('total')
        weekday = request.POST.get('weekday')
        # 插入数据
        if Class.objects.create(name=name, courseid=course,status=1,intro=info,place=place,time=time,count=count,teacherid=t,weekday=weekday,total=total):
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
        place = request.POST.get('place')
        time = request.POST.get('time')
        count = request.POST.get('count')
        course = request.POST.get('course')
        clasid = request.POST.get('clasid')
        total = request.POST.get('total')
        weekday = request.POST.get('weekday')
        if Class.objects.filter(classid=clasid).update(name=name,intro=info,courseid=course,place=place,time=time,count=count,weekday=weekday,total=total):
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
        classid = request.POST.get('classid')
        status = request.POST.get('status')
        if Class.objects.filter(classid=classid).update(status = status):
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

#获取专业以及课程信息
class GetAllMajorCourse(View):
    def get(self, request):
        majors = Major.objects.all().order_by('majorid').values()
        data = []
        children = []
        for i in majors:
            course = Course.objects.filter(majorid=i.get('majorid'))
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
#获取所有老师
class GetAllTeacher(View):
    def get(self,request):
        teachers = Teacher.objects.all()
        data = []
        for t in teachers:
            data.append({'value': t.teacherid,'label': t.name+'.'+t.account})
        return JsonResponse(data, safe=False)
#课程添加学生
class AddStudentTClass(View):
    def post(self,request):
        studentid = request.POST.get('studentid')
        classid = request.POST.get('classid')
        s = Classstu.objects.filter(studentid=Student.objects.get(studentid=studentid),classid=Class.objects.get(classid=classid))
        print(len(s))
        if len(s)!=0 and s[0].status==0:
            Classstu.objects.filter(studentid=Student.objects.get(studentid=studentid),classid=Class.objects.get(classid=classid)).update(status=1)
            data = {
                "status": 1,
                "result": "该学生已经添加",
                "data": None,
            }
            return JsonResponse(data)
        elif len(s)!=0 and s[0].status==1:
            data = {
                "status": 1,
                "result": "该学生已经添加",
                "data": None,
            }
            return JsonResponse(data)
        else:
            Classstu.objects.create(studentid=Student.objects.get(studentid=studentid),classid=Class.objects.get(classid=classid),status=1)
            data = {
                "status": 1,
                "result": "该学生已经添加",
                "data": None,
            }
            return JsonResponse(data)
#移除课程学生
class RemoveStudentClass(View):
    def post(self,request):
        studentid = request.POST.get('studentid')
        classid = request.POST.get('classid')
        if Classstu.objects.filter(classid=classid,studentid=studentid).update(status=0):
            data = {
                "status": 1,
                "result": "该学生已经移除",
                "data": None,
            }
            return JsonResponse(data)
        else:
            data = {
                "status": 1,
                "result": "该学生移除失败",
                "data": None,
            }
            return JsonResponse(data)