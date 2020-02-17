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
from android.view.HandleClass import *
from android.view.HandleFace import *
from android.view.HandleLogin import *
from android.view.HandleNews import *
from android.view.HandleWeather import *
from web import views as we
from web.view.HandleCategory import *
from web.view.HandleCheck import *
from web.view.HandleInfo import *
from web.view.HandleMajor import *
from web.view.HandleNew import *
from web.view.HandleStudent import *
from web.view.HandleTeacher import *
from web.view.HandleCourse import *
from web.view.HandleClass import *
from web.view.HandleTimer import *


from django.views import static ##新增
from django.conf import settings ##新增
from django.conf.urls import url ##新增

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('test/',av.test_view),
    url('ppp',av.ppp),
    #^以。。。开头$以。。。结尾
    url(r'^articles/2003/$',av.article),
    url(r'^articles/(?P<year>[0-9]{4})/$',av.article_archive),
    url("android/",include("android.urls")),
    #android端
    url(r'^android/login/$',Login.as_view()),
    #面部信息管理
    url(r'^android/facelogin/$', FaceLogin.as_view()),
    url(r'^android/recordfacedata/$',RecordFaceData.as_view()),
    #新闻管理
    url(r'^android/getTop5News/$',GetTop5News.as_view()),
    #天气管理
    url(r'^android/getWeather/$',GetWeather.as_view()),
    #课程表管理
    url(r'^android/getPClass/$',GetPerClass.as_view()),
    url(r'^android/getAllClass/$',GetAllClass.as_view()),
    url(r'^android/getClassInfo/$',GetClassInfo.as_view()),
    url(r'^android/getClassComment/$',GetClassComment.as_view()),
    url(r'^android/sendClassComment/$',SendClassComment.as_view()),
    #web端
    url(r'^web/login/$',we.login),
    #学生管理
    url(r'^web/userlist/$',StudentList.as_view()),
    url(r'^web/userlist/getAllMajor/',GetAllMajor.as_view()),
    url(r'^web/userlist/addstudent/',AddStudent.as_view()),
    url(r'^web/userlist/getAllStudents/',GetAllStudents.as_view()),
    url(r'^web/userlist/changestudent/',ChangeStudent.as_view()),
    url(r'^web/userlist/changestatus/',ChangeSStatus.as_view()),
    url(r'^web/userclasslist/$',GetClassStudent.as_view()),
    #教师管理
    url(r'^web/teacherList/$',TeacherList.as_view()),
    url(r'^web/teacherList/getAllMajor/',GetAllMajor.as_view()),
    url(r'^web/teacherList/addteacher/',AddTeacher.as_view()),
    url(r'^web/teacherList/changeteacher/', ChangeTeacher.as_view()),
    url(r'^web/teacherList/changeTstatus/', ChangeTStatus.as_view()),
    # url(r'^web/teacherList/searchTClass/', SearchTClass.as_view()),
    #课程管理
    url(r'^web/courseList/$',CourseList.as_view()),
    url(r'^web/courseList/getAllMajor/', GetAllMajor.as_view()),
    url(r'^web/courseList/addcourse/',AddCourse.as_view()),
    url(r'^web/courseList/changecourse/', ChangeCourse.as_view()),
    url(r'^web/courseList/changeCstatus/', ChangeCStatus.as_view()),
    #班级管理
    url(r'^web/classList/$', ClassList.as_view()),
    url(r'^web/classList/getAllMajor/', GetAllMajorCourse.as_view()),
    url(r'^web/classList/getAllTeacher/', GetAllTeacher.as_view()),
    url(r'^web/classList/getClassInfo/', GetSingleClass.as_view()),
    url(r'^web/classList/addclass/', AddClass.as_view()),
    url(r'^web/classList/changeclass/', ChangeClass.as_view()),
    url(r'^web/classList/changeCstatus/', ChangeClStatus.as_view()),
    url(r'^web/classList/addstudentTclass/', AddStudentTClass.as_view()),
    url(r'^web/classList/removeclassstudent/', RemoveStudentClass.as_view()),
    #课程管理
    url(r'^web/majorList/$', GetMajorList.as_view()),
    url(r'^web/majorList/addmajor/', AddMajor.as_view()),
    url(r'^web/majorList/changemajor/', ChangeMajor.as_view()),
    url(r'^web/majorList/changeMstatus/', ChangeMStatus.as_view()),
    #通知管理
    url(r'^web/MCCList/$', GetMCC.as_view()),
    url(r'^web/infoManage/sendMessage/', SendMessage.as_view()),
    url(r'^web/infoManage/getMessage/', GetMessage.as_view()),
    #考勤管理
    url(r'^web/checkList/$', CheckList.as_view()),
    url(r'^web/checkList/startCheck/', StartCheck.as_view()),
    url(r'^web/checkList/GetClassCheck/', GetClassCheck.as_view()),
    url(r'^web/checkList/GetDayCheck/', GetDayCheck.as_view()),
    #新闻种类管理
    url(r'^web/categoryList/$', GetCategoryList.as_view()),
    url(r'^web/categoryList/addcategory/', AddCategory.as_view()),
    url(r'^web/categoryList/changecategory/', ChangeCategory.as_view()),
    url(r'^web/categoryList/changeCstatus/', ChangeCateStatus.as_view()),
    #新闻管理
    url(r'^web/newList/$', GetNewList.as_view()),
    url(r'^web/newList/changeNstatus/', ChangeNewStatus.as_view()),
    url(r'^web/newList/addNew/', AddNew.as_view()),
    url(r'^web/newList/changeNew/', ChangeNew.as_view()),
    #定时器
    url(r'^web/Controller/weatherControl/$', WeatherControl.as_view()),
    #图片过滤
    url(r'^static/pic/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),

]
