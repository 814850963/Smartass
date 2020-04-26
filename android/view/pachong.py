# 处理json数据
import urllib
from urllib import request
import json

from django.http import JsonResponse
from django.views import View


class getdouban(View):
    def get(self,req):
        fid = req.GET.get('fid')
        url = 'https://api.douban.com/v2/movie/subject/'+fid+'?apikey=0df993c66c0c636e29ecbb5344252a4a#'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        req = request.Request(url, headers=headers)
        response = request.urlopen(req)
        if response.getcode() == 200:
            result = response.read()
            result = str(result, encoding='utf-8')
            print(result)
            return JsonResponse(result,safe=False)