from django.http import JsonResponse
from django.views import View


#获取专业信息
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
        majorsarray = []

        return JsonResponse(data[0],safe=False)
class SendMessage(View):
    def post(self,request):
        print(request.POST)
        classid = request.POST.get('classid')
        theme = request.POST.get('theme')
        content = request.POST.get('content')
        teacherid = request.POST.get('teacherid')
        c = Class.objects.get(classid=classid)
        t = Teacher.objects.get(teacherid=teacherid)
        info = Info.objects.create(classid=c,intro=content,name=theme,status=1,teacherid=t)
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