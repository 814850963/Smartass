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
#转化成json（数据丢失）
# students = json.loads(serializers.serialize("json", students))
FACE_URL = '/static/facedata/'
STUDENTPIC_URL = '/static/pic/'
PENGYOUQUAN_URL = '/static/pengyouquan/'
#获取学生列表
class StudentList(View):
    def get(self,request):
        page = request.GET.get('page')
        grade = request.GET.get('grade')
        major = request.GET.get('major')
        #带专业和页数查询
        if grade != None and major != None and page !=None:
            students = Student.objects.raw(
                'select s.*,m.mname from major m inner join student s  on s.majorid=' + major + ' and s.majorid = m.majorid and s.grade=' + grade)
            length = len(students)
            temp = []
            for s in students:
                temp.append(
                    {'sid':s.studentid,'account': s.account, 'name': s.name,'mname':s.mname, 'headpic': "http://"+request.get_host()+Utils.PIC_URL+s.headpic, 'grade': s.grade, 'email': s.email,
                     'major': s.majorid.majorid, 'status': s.status})
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[abs(int(page) - 1) * 10:abs(int(page) - 1) * 10 + 10],
                "page": abs(int(page)),
                "len": length
            }
            return JsonResponse(data)
        # 带专业查询
        elif page==None and grade!=None and major!=None:
            students = Student.objects.raw('select s.*,m.mname from major m inner join student s  on s.majorid='+major +' and s.majorid = m.majorid and s.grade='+grade)
            temp = []
            length = len(students)
            for s in students:
                temp.append(
                    {'sid':s.studentid,'account': s.account, 'name': s.name,'mname':s.mname, 'headpic': "http://"+request.get_host()+Utils.PIC_URL+s.headpic, 'grade': s.grade, 'email': s.email,
                     'major': s.majorid.majorid, 'status': s.status})
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[0:10],
                "page": 1,
                "len": length
            }
            return JsonResponse(data)
        #直接查询
        students = Student.objects.raw('select s.*,m.mname from major m inner join student s  on m.majorid=s.majorid')
        temp = []
        for s in students:
            temp.append({'sid':s.studentid,'account':s.account,'mname':s.mname,'name':s.name,'headpic': "http://"+request.get_host()+Utils.PIC_URL+s.headpic,'grade':s.grade,'email':s.email,'major':s.majorid.majorid,'status':s.status})
        length = len(students)
        data = {
            "status": 1,
            "result": "查询成功",
            "data": temp[abs(int(page)-1)*10:abs(int(page)-1)*10+10],
            "page": abs(int(page)),
            "len": length
        }
        return JsonResponse(data)

#获取专业信息
class GetAllMajor(View):
    def get(self, request):
        if(request.GET.get('flag')):
            majors = Major.objects.all().order_by('majorid').values()
            data = []
            for i in majors:
                instdata = {
                    'value': i.get('majorid'),
                    'label': i.get('mname')}
                data.append(instdata)
        else:
            majors = Major.objects.all().order_by('majorid').values()
            data = []
            for i in majors:
                instdata = {
                    'value': i.get('majorid'),
                    'label': i.get('mname'),
                    'children': [{
                        'value': '1',
                        'label': '大一'
                    }, {
                        'value': '2',
                        'label': '大二'
                    }, {
                        'value': '3',
                        'label': '大三'
                    }, {
                        'value': '4',
                        'label': '大四'
                    }]}
                data.append(instdata)
        instdata = {
            'value': 0,
            'label': '所有专业',}
        data.append(instdata)
        return JsonResponse(data,safe=False)

#添加学生
class AddStudent(View):
    def post(self,request):
        filename = request.POST.get('pic')
        file = request.FILES.get('file')
        name = request.POST.get('name')
        password = request.POST.get('password')
        account = request.POST.get('account')
        major = request.POST.get('major')
        grade = request.POST.get('grade')
        email = request.POST.get('email')
        #处理图片
        if not file:  # 文件对象不存在， 返回400请求错误
            data = {
                "status": 0,
                "result": "添加失败",
            }
            return JsonResponse(data)
        if filename.split('.')[-1] not in ['jpeg', 'jpg', 'png']:
            data = {
                "status": 0,
                "result": "文件格式有误",
            }
            return JsonResponse(data)
        #生成随机的名字
        filename = Utils.makerandomuuid(filename.split('.')[-1])
        #md5加密
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        result = md5.hexdigest()
        #生成major对象
        major = Major.objects.get(majorid=major)
        #插入数据
        Student.objects.create(name=name,passwd=result,account=account,majorid=major,grade=grade,headpic=filename,status=1,email=email)
        #保存文件
        with open(settings.STATIC_ROOT+ filename, 'wb+') as f:
            f.write(file.read())
        data = {
            "status": 1,
            "result": "添加成功",
        }
        return JsonResponse(data)

#修改学生信息
class ChangeStudent(View):
    def post(self, request):
        filename = request.POST.get('pic')
        file = request.FILES.get('file')
        name = request.POST.get('name')
        password = request.POST.get('password')
        account = request.POST.get('account')
        major = request.POST.get('major')
        grade = request.POST.get('grade')
        email = request.POST.get('email')
        sid = request.POST.get('sid')
        # 处理图片
        if not file:  # 文件对象不存在， 返回400请求错误
            data = {
                "status": 0,
                "result": "添加失败",
            }
            return JsonResponse(data)
        if filename.split('.')[-1] not in ['jpeg', 'jpg', 'png']:
            data = {
                "status": 0,
                "result": "文件格式有误",
            }
            return JsonResponse(data)
        # 生成随机的名字
        filename = Utils.makerandomuuid(filename.split('.')[-1])
        # md5加密
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        result = md5.hexdigest()
        # 生成major对象
        major = Major.objects.get(majorid=major)
        #获取原来用户的图片
        student = Student.objects.get(studentid=sid)
        f = student.headpic
        if f != 'null'and len(f)!=0:
            os.remove(settings.STATIC_ROOT+f)
        # 插入数据
        Student.objects.filter(studentid=sid).update(name=name, passwd=result, account=account, majorid=major, grade=grade, headpic=filename,email=email)
        # 保存文件
        with open(settings.STATIC_ROOT + filename, 'wb+') as f:
            f.write(file.read())
        data = {
            "status": 1,
            "result": "添加成功",
        }
        return JsonResponse(data)

#修改学生状态
class ChangeSStatus(View):
    def post(self,request):
        status = request.POST.get('status')
        sid = request.POST.get('sid')
        if Student.objects.filter(studentid=sid).update(status=status):
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
#获取上课的学生
class GetClassStudent(View):
    def get(self,request):
        page = request.GET.get('page')
        classid = request.GET.get('classid')
        if page!=None:
            #通过classid查询学生
            classtus = Classstu.objects.filter(classid=classid,status=1)
            students = []
            for s in classtus:
                students.append(s.studentid)
            studentlist = []
            for s in students:
                student = Student.objects.raw(
                    'select s.*,m.mname from major m inner join student s  on m.majorid=s.majorid and s.studentid = '+str(s.studentid))
                studentlist.append({'sid': student[0].studentid, 'account': student[0].account, 'mname': student[0].mname, 'name': student[0].name,
                             'headpic': "http://" + request.get_host() + Utils.PIC_URL + student[0].headpic, 'grade': student[0].grade,
                             'email': student[0].email, 'major': student[0].majorid.majorid, 'status': student[0].status})
            length = len(students)
            data = {
                "status": 1,
                "result": "查询成功",
                "data": studentlist[abs(int(page) - 1) * 10:abs(int(page) - 1) * 10 + 10],
                "page": abs(int(page)),
                "len": length
            }
            return JsonResponse(data)
        else:
            # 通过classid查询学生
            classtus = Classstu.objects.filter(classid=classid)
            students = []
            for s in classtus:
                print(s)
                students.append(s.studentid)
            studentlist = []
            for s in students:
                student = Student.objects.raw(
                    'select s.*,m.mname from major m inner join student s  on m.majorid=s.majorid and studentid = ' + s)
                studentlist.append(
                    {'sid': student.studentid, 'account': student.account, 'mname': student.mname, 'name': student.name,
                     'headpic': "http://" + request.get_host() + Utils.PIC_URL + student.headpic,
                     'grade': student.grade,
                     'email': student.email, 'major': student.majorid.majorid, 'status': student.status})
            length = len(students)
            data = {
                "status": 1,
                "result": "查询成功",
                "data": studentlist[0:10],
                "page": abs(int(page)),
                "len": length
            }
            return JsonResponse(data)
#获取所有学生
class GetAllStudents(View):
    def get(self,request):
        students = Student.objects.all()
        data = []
        for s in students:
            data.append({'value': s.studentid, 'label': s.name + '.' + s.account})
        return JsonResponse(data, safe=False)

