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
