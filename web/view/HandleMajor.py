
#获取专业列表
from django.http import JsonResponse
from django.views import View

from web.models import *


class GetMajorList(View):
    def get(self,request):
        page = request.GET.get('page')
        # 条件搜索
        if  page != None:
            majors = Major.objects.all()
            length = len(majors)
            temp = []
            for m in majors:
                temp.append(
                    {'majorid': m.majorid, 'name': m.mname, 'info': m.mintro, 'status': m.status})
            data = {
                "status": 1,
                "result": "查询成功",
                "data": temp[abs(int(page) - 1) * 10:abs(int(page) - 1) * 10 + 10],
                "page": abs(int(page)),
                "len": length
            }
            return JsonResponse(data)
        # 普通搜索
        majors = Major.objects.all()
        length = len(majors)
        temp = []
        for m in majors:
            temp.append(
                {'majorid': m.majorid, 'name': m.mname, 'info': m.mintro, 'status': m.status})
        data = {
            "status": 1,
            "result": "查询成功",
            "data": temp[0:10],
            "page": 1,
            "len": length
        }
        return JsonResponse(data)
#添加专业
class AddMajor(View):
    def post(self, request):
        name = request.POST.get('name')
        info = request.POST.get('info')
        # 插入数据
        if Major.objects.create(mname=name,  status=1, mintro=info):
            data = {
                "status": 1,
                "result": "添加成功",
            }
            return JsonResponse(data)
        else:
            data = {
                "status": 0,
                "result": "添加失败",
            }
            return JsonResponse(data)
#编辑专业
class ChangeMajor(View):
    def post(self,request):
        name = request.POST.get('name')
        info = request.POST.get('info')
        majorid = request.POST.get('mid')
        print(request.POST)
        if Major.objects.filter(majorid=majorid).update(mname=name, mintro=info):
            data = {
                "status": 1,
                "result": "修改成功",
            }
            return JsonResponse(data)
        else:
            data = {
                "status": 0,
                "result": "修改失败",
            }
            return JsonResponse(data)
#修改专业状态
class ChangeMStatus(View):
    def post(self,request):
        status = request.POST.get('status')
        majorid = request.POST.get('mid')
        if Major.objects.filter(majorid=majorid).update(status=status):
            data = {
                "status": 1,
                "result": "修改成功",
            }
            return JsonResponse(data)
        else:
            data = {
                "status": 0,
                "result": "修改失败",
            }
            return JsonResponse(data)