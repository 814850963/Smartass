from datetime import datetime

from django.http import JsonResponse
from django.views import View

#获取朋友圈动态
from android.models import *
from smartass import Utils, settings


class GetFriendShare(View):
    def shell_sort(self,a):
        n = len(a)
        gap = n >> 1  # gap是长度的一半
        while gap > 0:
            for i in range(gap, n):
                for j in range(i, 0, -gap):
                    if a[j].circleId < a[j - gap].circleId:
                        a[j], a[j - gap] = a[j - gap], a[j]
                    else:
                        break
            gap >>= 1  # gap每次减半

    def post(self,request):
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
        #关注的人
        followerstudent = []
        followerteacher = []
        fs = Follow.objects.filter(status=1,fid=auth,fidentify=identity)
        #获取所有朋友圈评论使用插入排序降序排列
        shares = []
        for f in fs:
            #关注者是学生
            if f.bfidentify == 1:
                followerstudent.append(Student.objects.get(studentid=f.bfid))
            #关注者是老师
            elif f.bfidentify == 2:
                followerteacher.append(Teacher.objects.get(teacherid=f.bfid))
        for s in followerstudent:
            #获取单个学生的所有朋友圈动态
            circles = Circle.objects.filter(studentid=s).order_by('-time')
            #把每个朋友圈都存进来
            for c in circles:
                shares.append(c)
        for t in followerteacher:
            # 获取单个教师的所有朋友圈动态
            circles = Circle.objects.filter(Teacherid=s).order_by('-time')
            # 把每个朋友圈都存进来
            for c in circles:
                shares.append(c)
        #希尔排序
        self.shell_sort(shares)
        data = []
        #封装数据
        for c in shares:
            lf = None
            #学生
            if identity=='1':
                islike = Circlelike.objects.filter(circleid=c,studentid=Student.objects.get(studentid=f.bfid),status=1)
                if islike == None:
                    lf = 0
                    pname = c.studentid.name
                else:
                    lf = 1
                    pname = c.studentid.name
            #老师
            elif identity == '2':
                islike = Circlelike.objects.filter(circleid=c,teacherid=Teacher.objects.get(teacherid=f.bfid),status=1)
                if islike == None:
                    lf = 0
                    pname = c.teacherid.name
                else:
                    lf = 1
                    pname = c.teacherid.name
            #获取头像
            if(c.studentid == None):
                pic = Utils.HOST+Utils.PIC_URL+Teacher.objects.filter(teacherid=c.teacherid.teacherid)[0].pic
            elif(c.teacherid == None):
                pic = Utils.HOST + Utils.PIC_URL + Student.objects.filter(studentid=c.studentid.studentid)[0].headpic
            data.append({
                'name':pname,
                'followid': c.circleid,
                'title': c.name,
                'intro': c.intro,
                'time': c.time,
                'pic': pic,
                'image':c.pic1,
                'zan':c.zan,
                'com':c.com,
                'islike':lf,
                'read':c.read
            })
        data = {
            "status": '1',
            "result": "添加成功",
            "data":data
        }
        return JsonResponse(data)

#获取我的动态
class GetMyShare(View):
    def post(self,request):
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
        if identity == '1':
            circles = Circle.objects.filter(studentid=auth).order_by('-circleid')
        elif identity == '0':
            circles = Circle.objects.filter(teacherid=auth).order_by('-circleid')
        # 封装数据
        data = []
        print(circles)
        for c in circles:
            lf = None
            # 学生
            if identity == '1':
                islike = Circlelike.objects.filter(circleid=c, studentid=Student.objects.get(studentid=auth),
                                                   status=1)
                if islike == None:
                    lf = 0
                    pname = c.studentid.name
                else:
                    lf = 1
                    pname = c.studentid.name
            # 老师
            elif identity == '2':
                islike = Circlelike.objects.filter(circleid=c, teacherid=Teacher.objects.get(teacherid=auth),
                                                   status=1)
                if islike == None:
                    lf = 0
                    pname = c.teacherid.name
                else:
                    lf = 1
                    pname = c.teacherid.name
            # 获取头像
            if (c.studentid == None):
                pic = Utils.HOST + Utils.PIC_URL + Teacher.objects.filter(teacherid=c.teacherid.teacherid)[0].pic
            elif (c.teacherid == None):
                pic = Utils.HOST + Utils.PIC_URL + Student.objects.filter(studentid=c.studentid.studentid)[0].headpic
            if c.pic1 == None:
                c.pic1 = ""
            image = Utils.HOST + Utils.PENGYOU_URL +c.pic1
            data.append({
                'name': pname,
                'followid': c.circleid,
                'title': c.name,
                'intro': c.intro,
                'time': c.time,
                'pic': pic,
                'image': image,
                'zan': c.zan,
                'com': c.com,
                'islike': lf,
                'read': c.read
            })
        print(data)
        data = {
            "status": '1',
            "result": "添加成功",
            "data":data
        }
        return JsonResponse(data)

#设置背景图片
class SetBackGround(View):
    def post(self,request):
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
        file = request.FILES.getlist("img","")
        filename = request.POST.get('pic')
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
        # 保存文件
        with open(settings.FRIEND_PIC + filename, 'wb+') as f:
            f.write(file[0].read())
        #学生
        if identity == '1':
            Student.objects.filter(studentid=auth).update(background=filename)
        #教师
        elif identity == '0':
            Teacher.objects.filter(teacherid=auth).update(background=filename)
        data = {
            "status": '1',
            "result": "添加成功",
            "data":{"background":Utils.HOST+Utils.PENGYOU_URL+filename}
        }
        return JsonResponse(data)
#发布朋友圈
class SendFMessage(View):
    def post(self,request):
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
        name = request.POST.get('name')
        intro = request.POST.get('intro')
        files = request.FILES.getlist("img","")
        print(request.POST)
        filenames = []
        #加入三个none
        filenames.append(None)
        filenames.append(None)
        filenames.append(None)
        for i,file in enumerate(files):
        # 处理图片
            if not file:  # 文件对象不存在， 返回400请求错误
                data = {
                    "status": 0,
                    "result": "添加失败",
                }
                return JsonResponse(data)
            if file.name.split('.')[-1] not in ['jpeg', 'jpg', 'png']:
                data = {
                    "status": 0,
                    "result": "文件格式有误",
                }
                return JsonResponse(data)
            # 生成随机的名字
            filename = Utils.makerandomuuid(file.name.split('.')[-1])
            filenames[i] = filename
        if identity == '1':
            student = Student.objects.get(studentid=auth)
            Circle.objects.create(studentid=student,status=1,name=str(name),intro=str(intro),time=datetime.now(),pic1=filenames[0],pic2=filenames[1],pic3=filenames[2],zan=0,com=0,read=0)
        elif identity == '0':
            teacher = Teacher.objects.get(teacherid=auth)
            Circle.objects.create(teacherid=teacher, status=1, name=str(name), intro=str(intro), time=datetime.now(),pic1=filenames[0],pic2=filenames[1],pic3=filenames[2],zan=0,com=0,read=0)
        # 保存文件
        for i,file in enumerate(files):
            with open(settings.FRIEND_PIC + filenames[i], 'wb+') as f:
                f.write(file.read())
        data = {
            "status": '1',
            "result": "添加成功",
        }
        return JsonResponse(data)