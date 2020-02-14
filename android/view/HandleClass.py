from django.http import JsonResponse
from django.views import View

from android.models import *


class GetPerClass(View):
    def post(self,request):
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
        print(request.POST)
        #身份为学生
        #获取所有正在上课的课程
        classes = []
        data = []
        if(identity=='1'):
            s = Student.objects.get(studentid=auth)
            stuclass = Classstu.objects.filter(studentid=s,status=1)
            for sc in stuclass:
                if sc.classid.status==1:
                    classes.append(sc.classid)
        for c in classes:
            #分割为星期几上课
            for weekday in c.weekday.split('/'):
                s,e = c.total.split('/')
                if weekday == '1':
                    weekday = 'mon'
                elif weekday == '2':
                    weekday = 'tue'
                elif weekday == '3':
                    weekday = 'web'
                elif weekday == '4':
                    weekday = 'thur'
                elif weekday == '5':
                    weekday = 'fri'
                elif weekday == '6':
                    weekday = 'sat'
                elif weekday == '7':
                    weekday = 'sun'
                data.append({
                    'classid':c.classid,
                    'name':c.name,
                    'intro':c.intro,
                    'courseid':c.courseid.courseid,
                    'place':c.place,
                    'time':c.time,
                    'count':c.count+c.time-1,
                    'teacherid':c.teacherid.teacherid,
                    'tname':Teacher.objects.get(teacherid=c.teacherid.teacherid).name,
                    'weekday':weekday,
                    'start':s,
                    'end':e
                })
        #身份为老师
        else:
            t = Teacher.objects.get(teacherid=auth)
            teaclass = Class.objects.filter(teacherid=t,status=1)
            for c in teaclass:
                # 分割为星期几上课
                for weekday in c.weekday.split('/'):
                    s, e = c.total.split('/')
                    if weekday == '1':
                        weekday = 'mon'
                    elif weekday == '2':
                        weekday = 'tue'
                    elif weekday == '3':
                        weekday = 'web'
                    elif weekday == '4':
                        weekday = 'thur'
                    elif weekday == '5':
                        weekday = 'fri'
                    elif weekday == '6':
                        weekday = 'sat'
                    elif weekday == '7':
                        weekday = 'sun'

                    data.append({
                        'classid': c.classid,
                        'name': c.name,
                        'intro': c.intro,
                        'courseid': c.courseid.courseid,
                        'place': c.place,
                        'time': c.time,
                        'count': c.count+c.time-1,
                        'teacherid': c.teacherid.teacherid,
                        'tname': t.name,
                        'weekday':weekday,
                        'start': s,
                        'end': e
                    })
        data = {
            "status": '1',
            "result": "添加成功",
            "data":data
        }
        return JsonResponse(data)