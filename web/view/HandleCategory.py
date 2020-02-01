from django.http import JsonResponse
from django.views import View

from web.models import *

#获取新闻种类列表
class GetCategoryList(View):
    def get(self,request):
        page = request.GET.get('page')
        categorys = Category.objects.all()
        categorylist = []
        for c in categorys:
            categorylist.append({'categoryid': c.categoryid,'name':c.name,'status':c.status })
        length = len(categorys)
        if int(page)>1:
            data = {
                "status": 1,
                "result": "查询成功",
                "data": categorylist[abs(int(page) - 1) * 10:abs(int(page) - 1) * 10 + 10],
                "page": abs(int(page)),
                "len": length
            }
        else:
            data = {
                "status": 1,
                "result": "查询成功",
                "data": categorylist[0:10],
                "page": abs(int(page)),
                "len": length
            }
        return JsonResponse(data)
#添加新闻种类
class AddCategory(View):
    def post(self,request):
        name = request.POST.get('name')
        Category.objects.create(name=name,status=1)
        data = {
            "status": 1,
            "result": "添加成功",
        }
        return JsonResponse(data)
#修改内容
class ChangeCategory(View):
    def post(self,request):
        cid = request.POST.get('cid')
        name = request.POST.get('name')
        Category.objects.filter(categoryid=cid).update(name=name)
        data = {
            "status": 1,
            "result": "修改成功",
        }
        return JsonResponse(data)
#修改状态
class ChangeCateStatus(View):
    def post(self,request):
        cid = request.POST.get('cid')
        status = request.POST.get('status')
        Category.objects.filter(categoryid=cid).update(status=status)
        data = {
            "status": 1,
            "result": "修改成功",
        }
        return JsonResponse(data)