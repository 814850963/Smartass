from django.http import JsonResponse
from django.views import View

from android.models import *


class GetWeather(View):
    def get(self,request):
        w = Weather.objects.filter().order_by('-weatherid')[0]
        if w != None:
            temp = {'temp':w.temp,'intro':w.intro,'pm':w.pm}
            data = {
                "status": "1",
                "result": "获取天气成功",
                "data":temp
            }
            return JsonResponse(data)
        else:
            data = {
                "status": "0",
                "result": "获取天气失败",
            }

            return JsonResponse(data)