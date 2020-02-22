import datetime

from django.http import JsonResponse
from django.views import View

from android.models import *
from smartass import Utils, settings
import time

class GetPerClass(View):
    def post(self,request):
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
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
                        weekday = 'wed'
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
                        weekday = 'wed'
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

#获取所有课程用于检索
class GetAllClass(View):
    def get(self,request):
        allclass = Class.objects.filter(status=1)
        data = []
        for c in allclass:
            s, e = c.total.split('/')
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
                'weekday':c.weekday,
                'start':s,
                'end':e
            })
        data = {
            "status": '1',
            "result": "添加成功",
            "data":data
        }
        return JsonResponse(data)

#获取课程信息
class GetClassInfo(View):
    def post(self,request):
        classid = request.POST.get('classid')
        c = Class.objects.get(classid=int(classid))
        data = ({
            'classid': c.classid,
            'name': c.name,
            'intro': c.intro,
            'courseid': c.courseid.courseid,
            'place': c.place,
            'time': c.time,
            'count': c.count + c.time - 1,
            'teacherid': c.teacherid.teacherid,
            'tname': Teacher.objects.get(teacherid=c.teacherid.teacherid).name,
            'weekday': c.weekday,
            'week':c.total
        })
        data = {
            "status": '1',
            "result": "添加成功",
            "data": data
        }
        return JsonResponse(data)

#获取课程评论
class GetClassComment(View):
    def post(self,request):
        classid = request.POST.get('classid')
        cs = Classcom.objects.filter(classid=int(classid),status=1)
        data=[]
        for c in cs:
            data.append({
                'intro': c.intro,
                'time': c.time,
                'studentid': c.studentid.studentid,
                'sname': c.studentid.name,
                'pic': Utils.HOST+Utils.PIC_URL+c.studentid.headpic,
            })
        data = {
            "status": '1',
            "result": "添加成功",
            "data": data
        }
        return JsonResponse(data)
#发表评论
class SendClassComment(View):
    def post(self,request):
        classid = request.POST.get('classid')
        auth = request.POST.get('auth')
        content = request.POST.get("content")
        s = Student.objects.get(studentid=auth)
        c = Class.objects.get(classid=classid)
        Classcom.objects.create(classid=c,studentid=s,status=1,time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),intro=content)
        data = {
            "status": '1',
            "result": "添加成功",
        }
        return JsonResponse(data)
#获取即将上课得信息
class GetInstantClass(View):
    def post(self,request):
        userid = request.POST.get('auth')
        u = Student.objects.get(studentid=userid)
        today = Util.objects.get(utilid=22)
        classes = Classstu.objects.filter(status=1,studentid=u)
        stuclas = []
        for c in classes:
            if c.classid.status == 1:
                stuclas.append(c.classid)
        c = None
        for cls in stuclas:
            weekday = cls.weekday.split('/')
            total = cls.total.split('/')
            #周数匹配
            if today.week <  int(total[1]) and today.week >= int(total[0]):
                #如果今天跟课程日期一样
                if str(today.weekday) in weekday:
                    #获取现在的时间
                    now = datetime.datetime.now()
                    #早上8点之前 0-23范围
                    if now.hour<8:
                        if cls.time == 1:
                            c=cls
                    elif now.hour<=9 and now.minute<=39:
                        if cls.time == 3:
                            c = cls
                    elif now.hour<13 and now.minute<=19:
                        if cls.time == 5:
                            c = cls
                    elif now.hour<15:
                        if cls.time == 7:
                            c = cls
                    elif now.hour<18:
                        if cls.time == 9:
                            c = cls
        if c !=None:
            if c.time == 1:
                c.time = "8:00"
            elif c.time == 3:
                c.time = "9:40"
            elif c.time == 5:
                c.time = "13:20"
            elif c.time == 7:
                c.time = "15:00"
            elif c.time == 9:
                c.time = "18:00"
            c = {"classid":c.classid,"name":c.name,"place":c.place,"tname":c.teacherid.name,"time":c.time}
        else:
            c = {"classid": None, "name": '今天没有课程哦', "place": "无教室", "tname": "无教师","time":"今天好好休息吧"}
        print(c)
        data = {
            "data" : c,
            "status": '1',
            "result": "添加成功",
        }
        return JsonResponse(data)
#检测考勤状态
class GetTeacherCheck(View):
    def post(self,request):
        print(request.POST)
        if request.POST.get("classid") == "null":
            data = {
                "status": '0',
                "result": "没有开启考勤",
            }
            return JsonResponse(data)
        classid = Class.objects.get(classid=request.POST.get("classid"))
        auth = request.POST.get("auth")
        #获取教师是否开启了考勤
        c = Check.objects.filter(classid=classid,status=1).order_by('-checkid')[0]
        if c == None:
            data = {
                "status": '0',
                "result": "没有开启考勤",
            }
            return JsonResponse(data)
        else:
            checkstu = Checkstu.objects.get(studentid=Student.objects.get(studentid=auth),checkid=c)
            if checkstu.status == 1:
                data = {
                    "status": '1',
                    "result": "已考勤",
                }
            else:
                data = {
                    "status": '2',
                    "result": "请考勤",
                }
        return JsonResponse(data)

