import base64
import datetime

from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views import View

from smartass import Utils, settings
from web.models import *


class GetNewList(View):
    def get(self,request):
        cid = request.GET.get('cid')
        news = New.objects.filter(categoryid=cid).order_by('-newid')
        temp = []
        for n in news:
            temp.append(
                {'newid': n.newid, 'name': n.name, 'intro':n.intro,'time':n.time, 'status': n.status})
        data = {
            "status": 1,
            "result": "查询成功",
            "data": temp,
        }
        return JsonResponse(data)
#添加新闻
class AddNew(View):
    def post(self,request):
        cid = request.POST.get('cid')
        theme = request.POST.get('theme')
        content = request.POST.get('content')
        # 获取时间以及转化
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        # 获取第一个图片
        index = content.find(';base64,')
        end = 0
        while index > 0:
            # 获取图片后缀
            sign = content[end:index].split('/')[-1]
            # 获取图片最后位置
            end = content.find('"', index)
            data = ContentFile(base64.b64decode(content[index + 8:end]),
                               name='temp.' + sign)  # You can save this as file instance.
            # 保存图片
            # 生成随机的名字
            filename = Utils.makerandomuuid(sign)
            # 保存文件
            with open(settings.NEW_PIC + filename, 'wb+') as f:
                f.write(data.read())
            # 把数据替换
            replaceindex = content[:index].find('src="')
            url = "http://" + request.get_host() + Utils.NEW_URL + filename
            content = content.replace(content[replaceindex + 5:end], url, 1)
            print(content)
            index = content.find(';base64,')
            print(index)
        new = New.objects.create(name=theme, status=1, categoryid=Category.objects.get(categoryid=cid),intro=content, time=now)
        if new:
            data = {
                "status": 1,
                "result": "新闻创建成功",
            }
            return JsonResponse(data)
        else:
            data = {
                "status": 0,
                "result": "新闻创建失败",
            }
            return JsonResponse(data)
#修改新闻
class ChangeNew(View):
    def post(self,request):
        cid = request.POST.get('cid')
        nid = request.POST.get('nid')
        theme = request.POST.get('theme')
        content = request.POST.get('content')
        # 获取时间以及转化
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        # 获取第一个图片
        index = content.find(';base64,')
        end = 0
        while index > 0:
            # 获取图片后缀
            sign = content[end:index].split('/')[-1]
            # 获取图片最后位置
            end = content.find('"', index)
            data = ContentFile(base64.b64decode(content[index + 8:end]),
                               name='temp.' + sign)  # You can save this as file instance.
            # 保存图片
            # 生成随机的名字
            filename = Utils.makerandomuuid(sign)
            # 保存文件
            with open(settings.NEW_PIC + filename, 'wb+') as f:
                f.write(data.read())
            # 把数据替换
            replaceindex = content[:index].find('src="')
            url = "http://" + request.get_host() + Utils.NEW_URL + filename
            content = content.replace(content[replaceindex + 5:end], url, 1)
            print(content)
            index = content.find(';base64,')
            print(index)
        new = New.objects.filter(newid=nid).update(name=theme, categoryid=Category.objects.get(categoryid=cid), intro=content,
                                 time=now)
        if new:
            data = {
                "status": 1,
                "result": "新闻修改成功",
            }
            return JsonResponse(data)
        else:
            data = {
                "status": 0,
                "result": "新闻修改失败",
            }
            return JsonResponse(data)
#修改新闻状态
class ChangeNewStatus(View):
    def post(self,request):
        nid = request.POST.get('nid')
        status = request.POST.get('status')
        New.objects.filter(newid=nid).update(status=status)
        data = {
            "status": 1,
            "result": "修改成功",
        }
        return JsonResponse(data)
