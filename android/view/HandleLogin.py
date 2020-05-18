import hashlib

from django.http import JsonResponse
from django.views import View

from android.models import *
from smartass import Utils, settings

class Login(View):
    def post(self,request):
        account = request.POST.get('account')
        password = request.POST.get("password")
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        result = md5.hexdigest()
        student = Student.objects.filter(account=account, passwd=result,status=1)
        if student:
            data = {
                "status": 1,
                "result": "登录成功",
                "auth": student[0].studentid,
                "name": student[0].name,
                "identity": 1,
                'intro': student[0].intro,
                'pic': Utils.HOST + Utils.PIC_URL+student[0].headpic,
            }
        else:
            teacher = Teacher.objects.filter(account=account, passwd=result)
            if teacher:
                data = {
                    "status": 1,
                    "result": "登录成功",
                    "auth": teacher[0].teacherid,
                    "name":teacher[0].name,
                    "identity": 0,
                    'intro': teacher[0].intro,
                    'pic': Utils.HOST + Utils.PIC_URL+teacher[0].pic,
                }
            else:
                data = {
                    "status": 0,
                    "result": "账号密码不正确",
                    "auth": None
                }
        print(data)
        return JsonResponse(data)

#获取个人信息(通过朋友圈说说点击)
class GetPersonProfile(View):
    def post(self,request):
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
        circleid =  request.POST.get('circleid')
        background = None
        flag = None
        course = None
        grade = None
        id = None
        iden = None
        print(request.POST)
        #获取本人跟点击人的关系
        if identity == '1' and circleid!=None:
            c = Circle.objects.get(circleid=circleid)
            #如果改人是学生
            if c.studentid != None:
                id = c.studentid.studentid
                iden = '1'
                f = Follow.objects.filter(fidentify=1,bfidentify=1,fid=auth,bfid=c.studentid.studentid)
                if len(f)!=0:
                    flag = f[0].status
                else:
                    flag = 0
                course = c.studentid.majorid.mname
                grade = c.studentid.grade
                if c.studentid.background != None:
                    background = Utils.HOST + Utils.PENGYOU_URL + c.studentid.background
                data = {
                    'id':id,
                    'iden':iden,
                    'name':  c.studentid.name,
                    'pic': Utils.HOST + Utils.PIC_URL + c.studentid.headpic,
                    'background': background,
                    'intro':  c.studentid.intro,
                    'islike':flag,
                    'course': course,
                    'grade':grade
                }
            #该人 是教师
            else:
                id = c.teacherid.teacherid
                iden = '0'
                f = Follow.objects.filter(fidentify=1,bfidentify=0,fid=auth,bfid=c.teacherid.teacherid)
                if len(f)!=0:
                    flag = f[0].status
                else:
                    flag = 0
                course = c.teacherid.majorid.mname
                grade = 0
                if c.teacherid.background != None:
                    background = Utils.HOST + Utils.PENGYOU_URL + c.teacherid.background
                data = {
                    'id':id,
                    'iden':iden,
                    'name': c.teacherid.name,
                    'pic': Utils.HOST + Utils.PIC_URL +c.teacherid.pic,
                    'background': background,
                    'intro': c.teacherid.intro,
                    'islike':flag,
                    'course': course,
                    'grade':grade
                }
        elif identity == '0' and circleid!=None:
            c = Circle.objects.get(circleid=circleid)
            #如果该人是学生
            if c.studentid != None:
                iden = '1'
                id = c.studentid.studentid
                f = Follow.objects.filter(fidentify=0,bfidentify=1,fid=auth,bfid=c.studentid.studentid)
                if len(f)!=0:
                    flag = f[0].status
                else:
                    flag = 0
                course = c.studentid.majorid.mname
                grade = c.studentid.grade
                if c.studentid.background != None:
                    background = Utils.HOST + Utils.PENGYOU_URL + c.studentid.background
                data = {
                    'id':id,
                    'iden':iden,
                    'name':  c.studentid.name,
                    'pic': Utils.HOST + Utils.PIC_URL + c.studentid.headpic,
                    'background': background,
                    'intro':  c.studentid.intro,
                    'islike':flag,
                    'course': course,
                    'grade':grade
                }
                print(data)
            #改任是教师
            else:
                iden = '0'
                id = c.teacherid.teacherid
                f = Follow.objects.filter(fidentify=0,bfidentify=0,fid=auth,bfid=c.teacherid.teacherid)
                if len(f)!=0:
                    flag = f[0].status
                else:
                    flag = 0
                course = c.teacherid.majorid.mname
                if c.teacherid.background != None:
                    background = Utils.HOST + Utils.PENGYOU_URL + c.teacherid.background
                grade = 0
                data = {
                    'id':id,
                    'iden':iden,
                    'name': c.teacherid.name,
                    'pic': Utils.HOST + Utils.PIC_URL +c.teacherid.pic,
                    'background': background,
                    'intro': c.teacherid.intro,
                    'islike':flag,
                    'course': course,
                    'grade':grade
                }
        if identity == '1' and circleid==None:
            s = Student.objects.get(studentid=auth)
            if s.background != None:
                background = Utils.HOST + Utils.PENGYOU_URL + s.background
            data = {
                'id':id,
                'iden':iden,
                'name': s.name,
                'pic': Utils.HOST + Utils.PIC_URL +s.headpic,
                'background':background,
                'intro': s.intro,
                'islike':flag,
                'course': course,
                'grade':grade
            }
        elif identity == '0' and circleid == None:
            t = Teacher.objects.get(teacherid=auth)
            if t.background != None:
                background = Utils.HOST + Utils.PENGYOU_URL + t.background
            data = {
                'id': id,
                'iden': iden,
                'name': t.name,
                'pic': Utils.HOST + Utils.PIC_URL +t.pic,
                'background': background,
                'intro': t.intro,
                'islike': flag,
                'course':course,
                'grade':grade
            }
        data = {
            "status": '1',
            "result": "成功",
            "data": data
        }
        return JsonResponse(data)
#获取个人信息(通过朋友搜索点击)
class GetFriendProfile(View):
    def post(self,request):
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
        iden = request.POST.get('iden')
        id = request.POST.get('id')
        f = Follow.objects.filter(fidentify=identity, bfidentify=iden, fid=auth, bfid=id)
        data = None
        background = None
        if iden == '1':
            s = Student.objects.get(studentid = id)
            if len(f) != 0:
                flag = f[0].status
            else:
                flag = 0
            course = s.majorid.mname
            grade = s.grade
            if s.background != None:
                background = Utils.HOST + Utils.PENGYOU_URL + s.background
            data = {
                'id': id,
                'iden': iden,
                'name': s.name,
                'pic': Utils.HOST + Utils.PIC_URL + s.headpic,
                'background': background,
                'intro': s.intro,
                'islike': flag,
                'course': course,
                'grade': grade
            }
        else:
            c = Teacher.objects.get(teacherid=id)
            if len(f) != 0:
                flag = f[0].status
            else:
                flag = 0
            course = c.majorid.mname
            if c.background != None:
                background = Utils.HOST + Utils.PENGYOU_URL + c.background
            grade = 0
            data = {
                'id': id,
                'iden': iden,
                'name': c.name,
                'pic': Utils.HOST + Utils.PIC_URL + c.pic,
                'background': background,
                'intro': c.intro,
                'islike': flag,
                'course': course,
                'grade': grade
            }
        data = {
            "status": '1',
            "result": "成功",
            "data": data
        }
        return JsonResponse(data)


#修改个人信息
class ChangeIntro(View):
    def post(self,request):
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
        intro = request.POST.get('intro')
        if identity == '1':
            Student.objects.filter(studentid=auth).update(intro=intro)
        else:
            Teacher.objects.filter(teacherid=auth).update(intro=intro)
        data = {
            "status": '1',
            "result": "成功",
        }
        return JsonResponse(data)