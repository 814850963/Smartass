"""smartass URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include

from android import views as av

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('test/',av.test_view),
    url('login/',av.login),
    url('ppp',av.ppp),
    #^以。。。开头$以。。。结尾
    url(r'^articles/2003/$',av.article),
    url(r'^articles/(?P<year>[0-9]{4})/$',av.article_archive),
    url("android/",include("android.urls"))

]
