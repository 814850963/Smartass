import datetime
import hashlib

from django.http import JsonResponse
from django.views import View

import base64

from django.core.files.base import ContentFile
#获取专业信息
from smartass import Utils, settings
from web.models import *


class GetMCC(View):
    def get(self, request):
        majors = Major.objects.all()
        data = []
        coursesarray = []
        majorsarray = []
        classsarray = []
        for m in majors:
            courses = Course.objects.filter(majorid=m)
            for c in courses:
                classes = Class.objects.filter(courseid=c)
                for cla in classes:
                    classsarray.append({
                        'value': cla.classid,
                        'label': cla.name,
                    })
                coursesarray.append({
                    'value': c.courseid,
                    'label': c.name,
                    'children':classsarray
                })
                classsarray = []
            majorsarray.append({
                'value': m.majorid,
                'label': m.mname,
                'children': coursesarray
            })
            coursesarray = []
        data.append(majorsarray)
        return JsonResponse(data[0],safe=False)
class SendMessage(View):
    def post(self,request):
        classid = request.POST.get('classid')
        theme = request.POST.get('theme')
        content = request.POST.get('content')
        teacherid = request.POST.get('teacherid')
        c = Class.objects.get(classid=classid)
        t = Teacher.objects.get(teacherid=teacherid)
        #获取时间以及转化
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        #获取第一个图片
        index = content.find(';base64,')
        end = 0
        while index>0:
            #获取图片后缀
            sign = content[end:index].split('/')[-1]
            #获取图片最后位置
            end = content.find('"',index)
            data = ContentFile(base64.b64decode(content[index+8:end]), name='temp.' + sign)  # You can save this as file instance.
            #保存图片
            # 生成随机的名字
            filename = Utils.makerandomuuid(sign)
            # 保存文件
            with open(settings.INFO_PIC + filename, 'wb+') as f:
                f.write(data.read())
            #把数据替换
            replaceindex = content[:index].find('src="')
            url = "http://" + request.get_host() + Utils.INFO_URL + filename
            content = content.replace(content[replaceindex+5:end],url,1)
            print(content)
            index = content.find(';base64,')
            print(index)
        info = Info.objects.create(classid=c,intro=content,name=theme,status=1,teacherid=t,date=now)
        if info:
            students = Classstu.objects.filter(classid=c)
            student = []
            for i in range(0,len(students)):
                student.append(students[i].studentid)
            for s in student:
              student = Student.objects.get(studentid=s.studentid)
              Infostu.objects.create(infoid=info,studentid=student,status=0)
            data = {
                "status": 1,
                "result": "消息发送成功",
            }
            return JsonResponse(data)
        else:
            data = {
                "status": 0,
                "result": "消息发送失败",
            }
            return JsonResponse(data)
class GetMessage(View):
    def get(self,request):
        print(request.GET)
        page = request.GET.get('page')
        classid = request.GET.get('classid')
        if page==0:
            page=1
        if page==None:
            messages = Info.objects.raw('select i.*,t.name as tname, c.name as cname from Info i inner join teacher t  on i.teacherid=t.teacherid inner join class c on i.classid=c.classid order by i.infoid desc')
            temp = []
            for m in messages:
                temp.append({'infoid': m.infoid, 'intro': m.intro, 'name': m.name, 'teacherid': m.teacherid.teacherid,
                             'classid': m.classid.classid,'teachername': m.tname, 'classname': m.cname, 'status': m.status})
            length = len(messages)
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[0:10],
                "page": 1,
                "len": length
            }
            return JsonResponse(data)
        elif page==None and classid!=None:
            messages = Info.objects.raw(
                'select i.*,t.name as tname, c.name as cname from Info i inner join teacher t  on i.teacherid=t.teacherid inner join class c on i.classid='+classid +' and c.classid = '+ classid +' order by i.infoid desc')
            temp = []
            for m in messages:
                temp.append({'infoid': m.infoid, 'intro': m.intro, 'name': m.name, 'teacherid': m.teacherid.teacherid,
                             'classid': m.classid.classid, 'teachername': m.tname, 'classname': m.cname,
                             'status': m.status})
            length = len(messages)
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[abs(int(page) - 1) * 10:abs(int(page) - 1) * 10 + 10],
                "page": abs(int(page)),
                "len": length
            }
            return JsonResponse(data)
        elif page != None and classid == None:
            messages = Info.objects.raw('select i.*,t.name as tname, c.name as cname from Info i inner join teacher t  on i.teacherid=t.teacherid inner join class c on i.classid=c.classid order by i.infoid desc')
            temp = []
            for m in messages:
                temp.append({'infoid': m.infoid, 'intro': m.intro, 'name': m.name, 'teacherid': m.teacherid.teacherid,
                             'classid': m.classid.classid, 'teachername': m.tname, 'classname': m.cname,
                             'status': m.status})
            length = len(messages)
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[abs(int(page) - 1) * 10:abs(int(page) - 1) * 10 + 10],
                "page": abs(int(page)),
                "len": length
            }
            return JsonResponse(data)
        elif page != None and classid != None:
            messages = Info.objects.raw(
                'select i.*,t.name as tname, c.name as cname from Info i inner join teacher t  on i.teacherid=t.teacherid inner join class c on i.classid='+classid +' and c.classid = '+ classid +' order by i.infoid desc')
            temp = []
            for m in messages:
                temp.append({'infoid': m.infoid, 'intro': m.intro, 'name': m.name, 'teacherid': m.teacherid.teacherid,
                             'classid': m.classid.classid, 'teachername': m.tname, 'classname': m.cname,
                             'status': m.status})
            length = len(messages)
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[abs(int(page) - 1) * 10:abs(int(page) - 1) * 10 + 10],
                "page": abs(int(page)),
                "len": length
            }
            return JsonResponse(data)