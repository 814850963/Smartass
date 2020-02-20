from django.http import JsonResponse
from django.views import View

#获取朋友圈动态
from android.models import *
from smartass import Utils


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
        print(shares)
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
        print(data)
        return JsonResponse(data)

#获取我的动态
class GetMyShare(View):
    def post(self,request):
        auth = request.POST.get('auth')
        identity = request.POST.get('identity')
        data = {
            "status": '1',
            "result": "添加成功",
        }
        return JsonResponse(data)