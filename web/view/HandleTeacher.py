import hashlib
import os

from django.http import JsonResponse,HttpResponse
from django.views import View

from smartass import Utils, settings
from web.models import *


#获取学生列表
class TeacherList(View):
    def get(self,request):
        page = request.GET.get('page')
        major = request.GET.get('major')
        #带专业和页数查询
        if major != None and page !=None:
            teachers = Teacher.objects.raw('select t.*,m.mname from major m inner join teacher t  on t.majorid=' + major + ' and t.majorid = m.majorid')
            length = len(teachers)
            temp = []
            for t in teachers:
                temp.append(
                    {'tid':t.teacherid,'account': t.account, 'name': t.name,'mname':t.mname, 'headpic': "http://"+request.get_host()+Utils.PIC_URL+t.pic,  'email': t.email,'major': t.majorid.majorid, 'status': t.status})
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[abs(int(page) - 1) * 10:abs(int(page) - 1) * 10 + 10],
                "page": abs(int(page)),
                "len": length
            }
            return JsonResponse(data)
        # 带专业查询
        elif page==None and  major!=None:
            teachers = Teacher.objects.raw('select t.*,m.mname from major m inner join teacher t  on t.majorid=' + major + ' and t.majorid = m.majorid')
            length = len(teachers)
            temp = []
            for t in teachers:
                temp.append(
                    {'tid': t.teacherid, 'account': t.account, 'name': t.name, 'mname': t.mname,'headpic': "http://" + request.get_host() + Utils.PIC_URL + t.pic, 'email': t.email,'major': t.majorid.majorid, 'status': t.status})
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[0:10],
                "page": 1,
                "len": length
            }
            return JsonResponse(data)
        #直接查询
        teachers = Teacher.objects.raw('select t.*,m.mname from major m inner join teacher t  on m.majorid=t.majorid')
        print(teachers)
        temp = []
        for t in teachers:
            temp.append({'tid': t.teacherid, 'account': t.account, 'name': t.name, 'mname': t.mname,'headpic': "http://" + request.get_host() + Utils.PIC_URL + t.pic, 'email': t.email,'major': t.majorid.majorid, 'status': t.status})
        length = len(teachers)
        data = {
            "status": 1,
            "result": "查询成功",
            "data": temp[abs(int(page)-1)*10:abs(int(page)-1)*10+10],
            "page": abs(int(page)),
            "len": length
        }
        return JsonResponse(data)

#添加老师
class AddTeacher(View):
    def post(self,request):
        print(request.POST)
        print(request.FILES)
        filename = request.POST.get('pic')
        file = request.FILES.get('file')
        name = request.POST.get('name')
        password = request.POST.get('password')
        account = request.POST.get('account')
        major = request.POST.get('major')
        email = request.POST.get('email')
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
        # 插入数据
        Teacher.objects.create(name=name, passwd=result, account=account, majorid=major, pic=filename,
                               status=1, email=email)
        # 保存文件
        with open(settings.STATIC_ROOT + filename, 'wb+') as f:
            f.write(file.read())
        data = {
            "status": 1,
            "result": "添加成功",
        }
        return JsonResponse(data)
#修改老师信息
class ChangeTeacher(View):
    def post(self, request):
        print(request.POST)
        filename = request.POST.get('pic')
        file = request.FILES.get('file')
        name = request.POST.get('name')
        password = request.POST.get('password')
        account = request.POST.get('account')
        major = request.POST.get('major')
        email = request.POST.get('email')
        tid = request.POST.get('tid')
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
        teacher = Teacher.objects.get(teacherid=tid)
        f = teacher.pic
        if f != 'null':
            os.remove(settings.STATIC_ROOT+f)
        # 插入数据
        Teacher.objects.filter(teacherid=tid).update(name=name, passwd=result, account=account, majorid=major, pic=filename,email=email)
        # 保存文件
        with open(settings.STATIC_ROOT + filename, 'wb+') as f:
            f.write(file.read())
        data = {
            "status": 1,
            "result": "添加成功",
        }
        return JsonResponse(data)
#修改老师状态
class ChangeTStatus(View):
    def post(self,request):
        status = request.POST.get('status')
        tid = request.POST.get('tid')
        if Teacher.objects.filter(teacherid=tid).update(status=status):
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
#获取老师所带班级信息
class SearchTClass:
    def get(self,request):
        pass