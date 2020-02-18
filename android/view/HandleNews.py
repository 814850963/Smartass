from django.http import JsonResponse
from django.views import View

from android.models import *
from smartass import Utils


class GetTop5News(View):
    def get(self,request):
        news = New.objects.filter(status=1).order_by('-time')
        temp = []
        for n in news:
            temp.append({'newid': n.newid, 'name': n.name, 'intro': n.intro, 'time': n.time,'status': n.status, 'categoryid': n.categoryid.categoryid,'pic':  Utils.HOST + Utils.NEW_URL  + n.pic})
        data = {
            "status": "1",
            "data":temp[0:5],
            "result": "获取新闻成功",
        }
        return JsonResponse(data)
#获取所有新闻标题
class GetAllNewTitle(View):
    def get(self,request):
        cates = Category.objects.filter(status=1)
        date = []
        for cat in cates:
            date.append({'categoryid': cat.categoryid, 'name': cat.name})
        data = {
            "status": "1",
            "data": date,
            "result": "获取新闻成功",
        }
        return JsonResponse(data)

#获取新标题的所有新闻
class GetNewsList(View):
    def post(self,request):
        categoryid = request.POST.get('categoryid')
        category = Category.objects.get(categoryid=int(categoryid))
        news = New.objects.filter(categoryid=category,status=1)
        data = []
        for n in news:
            data.append({'newid': n.newid,'name':n.name,'time':n.time,'pic':Utils.HOST + Utils.NEW_URL  + n.pic,'cname':n.categoryid.name})
        data = {
            "status": "1",
            "data": data,
            "result": "获取新闻成功",
        }
        return JsonResponse(data)
#获取单个新闻
class GetANew(View):
    def post(self,request):
        newid = request.POST.get('newid')
        n = New.objects.filter(newid=int(newid))[0]
        data = ({'newid': n.newid,'name':n.name, 'intro': n.intro.replace("http://localhost:8000",Utils.HOST),'time':n.time,'pic':Utils.HOST + Utils.NEW_URL  + n.pic,'cname':n.categoryid.name})
        data = {
            "status": "1",
            "data": data,
            "result": "获取新闻成功",
        }
        return JsonResponse(data)
