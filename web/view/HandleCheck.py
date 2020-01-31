import datetime

from django.http import JsonResponse
from django.views import View

from smartass import Utils
from web.models import *


class CheckList(View):
    def get(self,request):
        page = request.GET.get('page')
        classid = request.GET.get('classid')
        c = Class.objects.get(classid=classid)
        #获取数据
        checks = Check.objects.filter(classid=c).order_by('-checkid')
        length = len(checks)
        temp = []
        count = 0
        for c in checks:
            t = Teacher.objects.get(teacherid=c.teacherid.teacherid)
            temp.append(
                {'checkid':c.checkid,'time':c.time,'teacherid':t.teacherid,'teachername':t.name,'status':c.status})
            c = Class.objects.raw('select c.*,t.name as tname from class c inner join teacher t on c.teacherid = t.teacherid and c.classid= ' + str(c.classid.classid))
            c = c[0]
            temp[count]['tname'] = c.tname
            count += 1
        if page == 1:
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[0:10],
                "page": 1,
                "len": length
            }
        else:
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[abs(int(page) - 1) * 10:abs(int(page) - 1) * 10 + 10],
                "page": abs(int(page)),
                "len": length
            }
        return JsonResponse(data)

#开启考勤
class StartCheck(View):
    def post(self,request):
        classid = request.POST.get('classid')
        teacherid = request.POST.get('teacherid')
        if teacherid==None:
            teacherid = 6
        now = datetime.datetime.now()
        #创建考勤记录
        teacherid = Teacher.objects.filter(teacherid=teacherid, status=1)
        classid = Class.objects.filter(classid=classid, status=1)
        if not teacherid or not classid:
            data = {
                "status": 1,
                "result": "课程异常",
            }
            return JsonResponse(data)
        c = Check.objects.create(time=now,teacherid=teacherid[0],classid=classid[0],status=1)
        #先进行判断是否已经有考勤记录
        if Check.objects.filter(teacherid=teacherid[0],classid=classid[0]):
            data = {
                "status": 1,
                "result": "开启失败(已经开启过了)",
            }
            return JsonResponse(data)
        #通知学生考勤
        classtus = Classstu.objects.raw('select * from Classstu where classid='+classid+' and status=1')
        for clastu in classtus:
            Checkstu.objects.create(status=0,studentid=clastu.studentid,checkid=c)
        data = {
            "status": 1,
            "result": "开启成功",
        }
        return JsonResponse(data)
#获取这个课时的学生考勤数据
class GetClassCheck(View):
    def get(self,request):
        checkid = request.GET.get('checkid')
        #获取参与的所有学生
        checkstus = Checkstu.objects.filter(checkid=checkid).order_by('status')
        studentlist = []
        #打卡学生个数
        bad = 0
        good =0
        for cs in checkstus:
            studentid = str(cs.studentid.studentid)
            s = Student.objects.raw('select s.*,c.status as checkstatus from student s join checkstu c on s.studentid = '+studentid+' and c.studentid='+studentid)
            if s[0].checkstatus == 0:
                bad+=1
            else:
                good+=1
            studentlist.append({'sid': s[0].studentid, 'account': s[0].account, 'name': s[0].name,'headpic': "http://" + request.get_host() + Utils.PIC_URL + s[0].headpic,
                                'grade': s[0].grade,'email': s[0].email, 'major': s[0].majorid.majorid,'status': s[0].checkstatus})
        if Checkhistory.objects.filter(checkid=checkid):
            pass
        else:
            Checkhistory.objects.create(checkid=Check.objects.get(checkid=checkid),good=good,bad=bad)
        data = {
            "status": 1,
            "result": "查询成功",
            "data": studentlist,
            "good": good,
            "bad": bad
        }
        return JsonResponse(data)

