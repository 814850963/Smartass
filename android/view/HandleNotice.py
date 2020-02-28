import datetime

from django.http import JsonResponse
from django.views import View

from android.models import *

#获取所有通知
class GetAllNotice(View):
    def post(self,request):
        auth = request.POST.get('auth')
        identity = request.POST.get("identity")
        data = []
        # 学生
        if identity == '1':
            s = Student.objects.get(studentid=auth)
            si = Infostu.objects.filter(studentid=s).order_by('-infostu')
            if len(si) != 0:
                for i in si:
                    data.append({
                        "infoid": i.infoid.infoid,
                        "cname": i.infoid.classid.name,
                        "tname": i.infoid.teacherid.name,
                        "intro": i.infoid.intro,
                        "date": i.infoid.date,
                        "name":i.infoid.name
                    })
        # 教师
        else:
            t = Teacher.objects.get(teacherid=auth)
            infos = Info.objects.filter( teacherid=t, status=1).order_by('-date')
            for i in infos:
                data.append({
                    "infoid": i.infoid,
                    "cname": i.classid.name,
                    "tname": i.teacherid.name,
                    "intro": i.intro,
                    "date": i.date,
                    "name": i.name
                })
        data = {
            "status": '1',
            "result": "添加成功",
            "data": data
        }
        return JsonResponse(data)

#获取单个课程通知
class GetClassNotice(View):
    def post(self,request):
        classid = request.POST.get('classid')
        c = Class.objects.get(classid=classid)
        auth = request.POST.get('auth')
        identity = request.POST.get("identity")
        data = []
        #学生
        if identity=='1':
            s = Student.objects.get(studentid=auth)
            infos = Info.objects.filter(classid=c,status=1).order_by('-date')
            for i in infos:
                si = Infostu.objects.filter(infoid=i,studentid=s)
                if len(si)!=0:
                    data.append({
                        "infoid":i.infoid,
                        "cname":c.name,
                        "tname":i.teacherid.name,
                        "intro":i.intro,
                        "date":i.date,
                        "name":i.name
                    })
        #教师
        else:
            t = Teacher.objects.get(teacherid=auth)
            infos = Info.objects.filter(classid=c, teacherid=t,status=1).order_by('-date')
            for i in infos:
                data.append({
                    "infoid": i.infoid,
                    "cname": c.name,
                    "tname": i.teacherid.tname,
                    "intro": i.intro,
                    "date": i.date,
                    "name": i.name
                })
        data = {
            "status": '1',
            "result": "添加成功",
            "data": data
        }
        return JsonResponse(data)

#获取通知详情
class GetNoticeInfo(View):
    def post(self,request):
        infoid = request.POST.get('infoid')
        i = Info.objects.get(infoid=infoid)
        auth = request.POST.get('auth')
        identity = request.POST.get("identity")
        data = None
        #学生
        if identity == '1':
            infostu = Infostu.objects.get(infoid=i,studentid=Student.objects.get(studentid=auth))
            data = {
                    "infoid": i.infoid,
                    "title": i.name,
                    "tname": i.teacherid.name,
                    "intro": i.intro,
                    "time": i.date,
                    "status": infostu.status
                }
        #老师（未处理）
        else:
            pass
        print(data)
        data = {
            "status": '1',
            "result": "添加成功",
            "data": data
        }
        return JsonResponse(data)
#阅读
class CheckNotice(View):
    def post(self,request):
        infoid = request.POST.get('infoid')
        i = Info.objects.get(infoid=infoid)
        auth = request.POST.get('auth')
        identity = request.POST.get("identity")
        Infostu.objects.filter(infoid=i,studentid=Student.objects.get(studentid=auth)).update(status=1)
        data = {
            "status": '1',
            "result": "添加成功",
            "data": '1'
        }
        return JsonResponse(data)
#发送消息
class SendNoticeClass(View):
    def post(self,request):
        auth = request.POST.get('auth')
        identity = request.POST.get("identity")
        title = request.POST.get('title')
        intro = request.POST.get('intro')
        classid = request.POST.get('classid')
        print(request.POST)
        s = []
        clastu = Classstu.objects.filter(classid=classid,status=1)
        #获取课程学生
        if len(clastu)!=0:
            for cl in clastu:
                s.append(cl.studentid)
        #生成通知
        info = Info.objects.create(name=title,intro=intro,classid=Class.objects.get(classid=classid),teacherid=Teacher.objects.get(teacherid=auth),status=1,date=datetime.datetime.now())
        #把通知发送给学生
        for stu in s:
            Infostu.objects.create(infoid=info,studentid=stu,status=0)
        data = {
            "status": '1',
            "result": "添加成功",
            "data": '1'
        }
        return JsonResponse(data)





