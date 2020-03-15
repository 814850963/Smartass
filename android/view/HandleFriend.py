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
                    if a[j].circleid < a[j - gap].circleid:
                        a[j], a[j - gap] = a[j - gap], a[j]
                    else:
                        break
            gap >>= 1  # gap每次减半

    def post(self,request):
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
        print(request.POST)
        #关注的人
        followerstudent = []
        followerteacher = []
        fs = Follow.objects.filter(status=1,fid=auth,fidentify=identity)
        #获取所有朋友圈评论使用希尔排序降序排列
        shares = []
        for f in fs:
            #关注者是学生
            if f.bfidentify == 1:
                followerstudent.append(Student.objects.get(studentid=f.bfid))
            #关注者是老师
            elif f.bfidentify == 0:
                followerteacher.append(Teacher.objects.get(teacherid=f.bfid))
        for s in followerstudent:
            #获取单个学生的所有朋友圈动态
            circles = Circle.objects.filter(studentid=s).order_by('-time')
            #把每个朋友圈都存进来
            for c in circles:
                shares.append(c)
        for t in followerteacher:
            # 获取单个教师的所有朋友圈动态
            circles = Circle.objects.filter(Teacherid=t).order_by('-time')
            # 把每个朋友圈都存进来
            for c in circles:
                shares.append(c)
        #希尔排序
        self.shell_sort(shares)
        data = []
        #封装数据
        for c in shares:
            #获取头像
            if(c.studentid == None):
                pname = c.teacherid.name
                pic = Utils.HOST+Utils.PIC_URL+Teacher.objects.filter(teacherid=c.teacherid.teacherid)[0].pic
            elif(c.teacherid == None):
                pname = c.studentid.name
                pic = Utils.HOST + Utils.PIC_URL + Student.objects.filter(studentid=c.studentid.studentid)[0].headpic
            if identity == '1':
                flag = Circlelike.objects.filter(circleid=c, studentid=Student.objects.get(studentid=auth))
            else:
                flag = Circlelike.objects.filter(circleid=c, teacherid=Teacher.objects.get(teacherid=auth))
            if len(flag) == 0:
                flag = 0
            elif flag[0].status == 0:
                flag = 0
            else:
                flag = 1
            data.append({
                'circleid': c.circleid,
                'name':pname,
                'followid': c.circleid,
                'title': c.name,
                'intro': c.intro,
                'time': c.time.strftime('%Y-%m-%d %H:%I:%S'),
                'pic': pic,
                'image':c.pic1,
                'zan':c.zan,
                'com':c.com,
                'read':c.read,
                'islike': flag
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
        if request.POST.get('iden')!=None:
            identity = request.POST.get('iden')
        if request.POST.get('id') != None:
            auth = request.POST.get('id')
        print(request.POST)
        if identity == '1':
            circles = Circle.objects.filter(studentid=auth,status=1).order_by('-circleid')
        elif identity == '0':
            circles = Circle.objects.filter(teacherid=auth,status=1).order_by('-circleid')
        # 封装数据
        data = []
        for c in circles:
            # 学生
            if identity == '1':
                    pname = c.studentid.name
            # 老师
            elif identity == '0':
                    pname = c.teacherid.name
            # 获取头像
            if (c.studentid == None):
                pic = Utils.HOST + Utils.PIC_URL + Teacher.objects.filter(teacherid=c.teacherid.teacherid)[0].pic
            elif (c.teacherid == None):
                pic = Utils.HOST + Utils.PIC_URL + Student.objects.filter(studentid=c.studentid.studentid)[0].headpic
            if c.pic1 == None:
                c.pic1 = ""
            image = Utils.HOST + Utils.PENGYOU_URL +c.pic1
            if identity == '1':
                flag = Circlelike.objects.filter(circleid=c, studentid=Student.objects.get(studentid=auth))
            else:
                flag = Circlelike.objects.filter(circleid=c, teacherid=Teacher.objects.get(teacherid=auth))
            if len(flag) == 0:
                flag = 0
            elif flag[0].status == 0:
                flag = 0
            else:
                flag = 1
            data.append({
                'circleid':c.circleid,
                'name': pname,
                'followid': c.circleid,
                'title': c.name,
                'intro': c.intro,
                'time': c.time.strftime('%Y-%m-%d %H:%I:%S'),
                'pic': pic,
                'image': image,
                'zan': c.zan,
                'com': c.com,
                'read': c.read,
                'islike': flag
            })
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
#获取单个朋友圈动态以及评论
class GetFriendInfo(View):
    def post(self,request):
        circleid = request.POST.get('circleid')
        circle = Circle.objects.get(circleid=circleid)
        c = None
        s = None
        t = None
        if circle.studentid != None:
            Circle.objects.filter(circleid=circleid).update(read=circle.read+1)
            s = circle.studentid
            c = circle
            if c.pic1 !=None:
                c.pic1 = Utils.HOST+Utils.PENGYOU_URL+c.pic1
            if c.pic2 !=None:
                c.pic2 = Utils.HOST+Utils.PENGYOU_URL+c.pic2
            if c.pic3 !=None:
                c.pic3 = Utils.HOST+Utils.PENGYOU_URL+c.pic3
            data = {"ppic":Utils.HOST+Utils.PIC_URL+s.headpic,"pname":s.name,"cname":c.name,"intro":c.intro,"time":c.time.strftime('%Y-%m-%d %H:%I:%S'),"pic1":c.pic1,"pic2":c.pic2,"pic3":c.pic3}
        elif Circle.objects.get(circleid=circleid).teacherid != None:
            Circle.objects.filter(circleid=circleid).update(read=circle.read + 1)
            t = circle.teacherid
            c = circle
            if c.pic1 !=None:
                c.pic1 = Utils.HOST+Utils.PENGYOU_URL+c.pic1
            if c.pic2 !=None:
                c.pic2 = Utils.HOST+Utils.PENGYOU_URL+c.pic2
            if c.pic3 !=None:
                c.pic3 = Utils.HOST+Utils.PENGYOU_URL+c.pic3
            data = {"ppic":Utils.HOST+Utils.PIC_URL+t.pic,"pname":t.name,"cname":c.name,"intro":c.intro,"time":c.time.strftime('%Y-%m-%d %H:%I:%S'),"pic1":c.pic1,"pic2":c.pic2,"pic3":c.pic3}
        data = {
            "status": '1',
            "result": "添加成功",
            "data":data
        }
        return JsonResponse(data)
#获取所有评论
class GetFriendComment(View):
    def shell_sort(self,a):
        n = len(a)
        gap = n >> 1  # gap是长度的一半
        while gap > 0:
            for i in range(gap, n):
                for j in range(i, 0, -gap):
                    if a[j].get('circommonid') > a[j - gap].get('circommonid'):
                        a[j], a[j - gap] = a[j - gap], a[j]
                    else:
                        break
            gap >>= 1  # gap每次减半
    def post(self,request):
        circleid = request.POST.get('circleid')
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
        data = []
        #获取这个朋友圈的评论
        cc = Circlecom.objects.filter(status=1, circleid=circleid).order_by('-time')
        # 获取所有朋友圈评论使用希尔排序降序排列
        shares = []
        for c in cc:
            # 发布者者是学生
            if c.studentid != None:
                flag = Circomlike.objects.filter(circlecomid=c.circommonid,studentid=auth)
                if len(flag) !=0:
                    flag = flag[0].status
                else:
                    flag = 0
                data.append({"circommonid":c.circommonid,"name":c.studentid.name,"pic":Utils.HOST+Utils.PIC_URL+c.studentid.headpic,"intro":c.intro,"zan":c.zan,"flag":flag})
            # 发布者是教师
            elif c.teacherid != None:
                flag = Circomlike.objects.filter(circlecomid=c.circommonid, teacherid=auth)
                if len(flag) !=0:
                    flag = flag[0].status
                else:
                    flag = 0
                data.append({"circommonid":c.circommonid,"name": c.teacherid.name, "pic": Utils.HOST + Utils.PIC_URL + c.teacherid.pic,
                             "intro": c.intro, "zan": c.zan, "flag": flag})
        # 希尔排序
        self.shell_sort(data)
        data = {
            "status": '1',
            "result": "添加成功",
            "data":data
        }
        return JsonResponse(data)
# 朋友圈点赞
class FriendCircleLike(View):
    def post(self,request):
        circleid = request.POST.get('circleid')
        c = Circle.objects.get(circleid=circleid)
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
        if identity == '1':
            auth = Student.objects.get(studentid=auth)
            if len(Circlelike.objects.filter(circleid=c, studentid=auth)) != 0:
                com = Circlelike.objects.filter(circleid=c, studentid=auth)[0]
                if com.status == 0:
                    Circlelike.objects.filter(circleid=c, studentid=auth).update(status=1)
                    Circle.objects.filter(circleid=circleid).update(zan=c.zan + 1)
                    f = 1
                else:
                    Circlelike.objects.filter(circleid=c, studentid=auth).update(status=0)
                    Circle.objects.filter(circleid=circleid).update(zan=c.zan - 1)
                    f = 0
            else:
                Circlelike.objects.create(circleid=c, studentid=auth, status=1)
                Circle.objects.filter(circleid=circleid).update(zan=c.zan + 1)
                f = 1
        else:
            auth = Teacher.objects.get(teacherid=auth)
            if len(Circlelike.objects.filter(circleid=c, teacherid=auth)) != 0:
                com = Circlelike.objects.filter(circleid=c, teacherid=auth)[0]
                if com.status == 0:
                    Circlelike.objects.filter(circleid=c, teacherid=auth).update(status=1)
                    Circle.objects.filter(circleid=circleid).update(zan=c.zan + 1)
                    f = 1
                else:
                    Circlelike.objects.filter(circleid=c, teacherid=auth).update(status=0)
                    Circle.objects.filter(circleid=circleid).update(zan=c.zan - 1)
                    f = 0
            else:
                Circlelike.objects.create(circleid=c, teacherid=auth, status=1)
                Circle.objects.filter(circleid=circleid).update(zan=c.zan + 1)
                f = 1
        data = {
            "status": '1',
            "result": "添加成功",
            "data": str(f)
        }
        return JsonResponse(data)

#朋友圈评论点赞
class FriendComLike(View):
    def post(self, request):
        c = request.POST.get('circommonid')
        circommonid = Circlecom.objects.filter(circommonid=c)[0]
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
        f = None
        #学生
        if identity == '1':
            auth = Student.objects.get(studentid=auth)
            if len(Circomlike.objects.filter(circlecomid=circommonid,studentid=auth))!=0:
                com = Circomlike.objects.filter(circlecomid=circommonid,studentid=auth)[0]
                if com.status==0:
                    Circomlike.objects.filter(circlecomid=circommonid, studentid=auth).update(status=1)
                    Circlecom.objects.filter(circommonid=c).update(zan=circommonid.zan+1)
                    f=1
                else:
                    Circomlike.objects.filter(circlecomid=circommonid, studentid=auth).update(status=0)
                    Circlecom.objects.filter(circommonid=c).update(zan=circommonid.zan - 1)
                    f=0
            else:
                Circomlike.objects.create(circlecomid=circommonid,studentid=auth,status=1)
                Circlecom.objects.filter(circommonid=c).update(zan=circommonid.zan + 1)
                f=1
        else:
            auth = Teacher.objects.get(teacherid=auth)
            if len(Circomlike.objects.filter(circlecomid=circommonid,teacherid=auth))!=0:
                com = Circomlike.objects.filter(circlecomid=circommonid,teacherid=auth)[0]
                if com.status==0:
                    Circomlike.objects.filter(circlecomid=circommonid, teacherid=auth).update(status=1)
                    Circlecom.objects.filter(circommonid=c).update(zan=circommonid.zan + 1)
                    f=1
                else:
                    Circomlike.objects.filter(circlecomid=circommonid, teacherid=auth).update(status=0)
                    Circlecom.objects.filter(circommonid=c).update(zan=circommonid.zan - 1)
                    f=0
            else:
                Circomlike.objects.create(circlecomid=circommonid, teacherid=auth, status=1)
                Circlecom.objects.filter(circommonid=c).update(zan=circommonid.zan + 1)
                f=1
        data = {
            "status": '1',
            "result": "添加成功",
            "data": str(f)
        }
        return JsonResponse(data)
#发布评论
class SendFriendComment(View):
    def post(self,request):
        circleid = request.POST.get('circleid')
        auth = request.POST.get('auth')
        content = request.POST.get('content')
        identity = request.POST.get('identity')
        if identity == '1':
            Circlecom.objects.create(circleid=Circle.objects.get(circleid=circleid),studentid=Student.objects.get(studentid=auth),status=1,zan=0,time=datetime.now().strftime('%Y-%m-%d %H:%I:%S'),intro=content)
        else:
            Circlecom.objects.create(circleid=Circle.objects.get(circleid=circleid),teacherid=Teacher.objects.get(teacherid=auth), status=1, zan=0,time=datetime.now().strftime('%Y-%m-%d %H:%I:%S'), intro=content)
        data = {
            "status": '1',
            "result": "添加成功",
        }
        return JsonResponse(data)
#获取关注的人
class GetPerLike(View):
    def post(self,request):
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
        data = []
        if identity == '1':
            fs = Follow.objects.filter(fid=auth,fidentify=1,status=1)
            for f in fs:
                #如果被关注的人是教师
                if f.bfidentify == 0:
                    t = Teacher.objects.get(teacherid=f.bfid)
                    data.append({
                        'id':t.teacherid,
                        "name": t.name,
                        "pic": Utils.HOST + Utils.PIC_URL + t.pic,
                        "iden": '0'
                    })
                else:
                    s = Student.objects.get(studentid=f.bfid)
                    data.append({
                        'id': s.studentid,
                        "name": s.name,
                        "pic": Utils.HOST + Utils.PIC_URL + s.headpic,
                        "iden": '1'
                    })
        else:
            fs = Follow.objects.filter(fid=auth, fidentify=0, status=1)
            for f in fs:
                # 如果被关注的人是教师
                if f.bfidentify == 0:
                    t = Teacher.objects.get(teacherid=f.bfid)
                    data.append({
                        'id': t.teacherid,
                        "name": t.name,
                        "pic": Utils.HOST + Utils.PIC_URL + t.pic,
                        "iden": '0'
                    })
                else:
                    s = Student.objects.get(studentid=f.bfid)
                    data.append({
                        'id': s.studentid,
                        "name": s.name,
                        "pic": Utils.HOST + Utils.PIC_URL + s.headpic,
                        "iden": '1'
                    })
        data = {
            "status": '1',
            "result": "添加成功",
            "data":data
        }
        return JsonResponse(data)

#关注某人
class FollowPerson(View):
    def post(self,request):
        id = request.POST.get('id')
        auth = request.POST.get('auth')
        iden = request.POST.get('iden')
        identity = request.POST.get('identity')
        f = Follow.objects.filter(fid=auth,bfid=id,fidentify=identity,bfidentify=iden)
        #如果有数据
        if len(f)!= 0:
            if f[0].status == 0:
                Follow.objects.filter(fid=auth, bfid=id, fidentify=identity, bfidentify=iden).update(status=1)
                data = {
                    "status": '1',
                    "result": "添加成功",
                    "data": '1'
                }
            else:
                Follow.objects.filter(fid=auth, bfid=id, fidentify=identity, bfidentify=iden).update(status=0)
                data = {
                    "status": '1',
                    "result": "添加成功",
                    "data": '0'
                }
        else:
            Follow.objects.create(fid=auth, bfid=id, fidentify=identity, bfidentify=iden,status=1)
            data = {
                "status": '1',
                "result": "添加成功",
                "data": '1'
            }
        return JsonResponse(data)
#搜索好友
class SearchFriend(View):
    def post(self,request):
        searchinfo = request.POST.get("searchinfo")
        data = []
        if len(Student.objects.filter(name__icontains=searchinfo)) != 0:
            for stu in Student.objects.filter(name__icontains=searchinfo):
                data.append({
                    'id':stu.studentid,
                    'iden':'1',
                    'name':stu.name,
                    'pic':Utils.HOST+Utils.PIC_URL+stu.headpic
                })
        if len(Teacher.objects.filter(name__icontains=searchinfo)) != 0:
            for tea in Teacher.objects.filter(name__icontains=searchinfo):
                data.append({
                    'id': tea.teacherid,
                    'iden': '0',
                    'name': tea.name,
                    'pic': Utils.HOST + Utils.PIC_URL + tea.pic
                })
        data = {
            "status": '1',
            "result": "添加成功",
            "data": data
        }
        return JsonResponse(data)