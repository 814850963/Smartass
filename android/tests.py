# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from android import models
import hashlib
s = models.Student(
    account= '3333',
    name='排序',
    passwd= hashlib.md5('123'.encode(encoding='UTF-8').hex()),
    headpic='null',
    facedata='null',
    majorid='1',
    grade='1',
    email='814850963@qq.com',
    intro="大二学长",
    status=1
)
s.save()