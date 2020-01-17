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
from web import views as we
from web.view.HandleStudent import *
from web.view.HandleTeacher import *
from web.view.HandleCourse import *
from web.view.HandleClass import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('test/',av.test_view),
    url('ppp',av.ppp),
    #^以。。。开头$以。。。结尾
    url(r'^articles/2003/$',av.article),
    url(r'^articles/(?P<year>[0-9]{4})/$',av.article_archive),
    url("android/",include("android.urls")),
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
    url(r'^web/classList/addclass/', AddClass.as_view()),
    url(r'^web/classList/changeclass/', ChangeClass.as_view()),
    url(r'^web/classList/changeCstatus/', ChangeClStatus.as_view()),
    url(r'^web/classList/addstudentTclass/', AddStudentTClass.as_view()),
    url(r'^web/classList/removeclassstudent/', RemoveStudentClass.as_view()),

]
