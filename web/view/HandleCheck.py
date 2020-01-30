from django.http import JsonResponse
from django.views import View

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
            t = Teacher.objects.get(teacherid=c.teacherid)
            temp.append(
                {'checkid':c.checkid,'time':c.time,'teacherid':c.teacherid,'teachername':t.name,'status':c.status})
            c = Class.objects.raw(
                'select c.*,t.name as tname from class c inner join teacher t on c.teacherid = t.teacherid and c.classid= ' + str(
                    c.classid))
            c = c[0]
            temp[count]['tname'] = c.tname
            print(temp[count])
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
