# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Admin(models.Model):
    adminid = models.AutoField(db_column='adminId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255)
    passwd = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin'


class Category(models.Model):
    categoryid = models.AutoField(db_column='categoryId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class Circle(models.Model):
    circleid = models.AutoField(db_column='circleId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255)
    intro = models.CharField(max_length=255)
    time = models.DateTimeField()
    status = models.IntegerField(blank=True, null=True)
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='studentId')  # Field name made lowercase.
    pic1 = models.CharField(max_length=255, blank=True, null=True)
    pic2 = models.CharField(max_length=255, blank=True, null=True)
    pic3 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'circle'


class Circlecom(models.Model):
    circommonid = models.AutoField(db_column='circommonId', primary_key=True)  # Field name made lowercase.
    intro = models.CharField(max_length=255)
    time = models.DateTimeField()
    status = models.IntegerField(blank=True, null=True)
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='studentId')  # Field name made lowercase.
    circleid = models.ForeignKey(Circle, models.DO_NOTHING, db_column='circleId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'circlecom'


class Circlelike(models.Model):
    circlelikeid = models.AutoField(db_column='circlelikeId', primary_key=True)  # Field name made lowercase.
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='studentId')  # Field name made lowercase.
    num = models.IntegerField(blank=True, null=True)
    circleid = models.ForeignKey(Circle, models.DO_NOTHING, db_column='circleId')  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'circlelike'


class Circomlike(models.Model):
    circlecomlikeid = models.AutoField(db_column='circlecomlikeId', primary_key=True)  # Field name made lowercase.
    num = models.IntegerField(blank=True, null=True)
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='studentId')  # Field name made lowercase.
    circlecomid = models.ForeignKey(Circlecom, models.DO_NOTHING, db_column='circlecomId')  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'circomlike'


class Class(models.Model):
    classid = models.AutoField(db_column='classId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255)
    intro = models.CharField(max_length=255)
    status = models.IntegerField(blank=True, null=True)
    courseid = models.ForeignKey('Course', models.DO_NOTHING, db_column='courseId', blank=True, null=True)  # Field name made lowercase.
    place = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    teacherid = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='teacherId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'class'


class Classcom(models.Model):
    classcomid = models.AutoField(db_column='classcomId', primary_key=True)  # Field name made lowercase.
    intro = models.CharField(max_length=255)
    time = models.DateTimeField()
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='studentId')  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classcom'


class Classstu(models.Model):
    classstu = models.AutoField(primary_key=True)
    classid = models.ForeignKey(Class, models.DO_NOTHING, db_column='classId')  # Field name made lowercase.
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='studentId')  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classstu'


class Course(models.Model):
    courseid = models.AutoField(db_column='courseId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255)
    intro = models.CharField(max_length=255)
    status = models.IntegerField()
    majorid = models.ForeignKey('Major', models.DO_NOTHING, db_column='majorid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course'


class Coursestu(models.Model):
    coursestuid = models.AutoField(db_column='coursestuId', primary_key=True)  # Field name made lowercase.
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='studentId')  # Field name made lowercase.
    courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='courseId')  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coursestu'


class Follow(models.Model):
    followid = models.AutoField(db_column='followId', primary_key=True)  # Field name made lowercase.
    fid = models.IntegerField(db_column='fId')  # Field name made lowercase.
    bfid = models.IntegerField(db_column='bfId')  # Field name made lowercase.
    fidentify = models.IntegerField()
    bfidentify = models.IntegerField()
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'follow'


class Info(models.Model):
    infoid = models.AutoField(db_column='infoId', primary_key=True)  # Field name made lowercase.
    intro = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    teacherid = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='teacherId')  # Field name made lowercase.
    classid = models.ForeignKey(Class, models.DO_NOTHING, db_column='classId')  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'info'


class Infostu(models.Model):
    infostu = models.AutoField(primary_key=True)
    infoid = models.ForeignKey(Info, models.DO_NOTHING, db_column='infoId')  # Field name made lowercase.
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='studentId')  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'infostu'


class Major(models.Model):
    majorid = models.AutoField(db_column='majorId', primary_key=True)  # Field name made lowercase.
    mname = models.CharField(max_length=255)
    mintro = models.CharField(max_length=255)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'major'


class New(models.Model):
    newid = models.AutoField(db_column='newId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255)
    intro = models.CharField(max_length=255)
    pic = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'new'


class Student(models.Model):
    studentid = models.AutoField(db_column='studentId', primary_key=True)  # Field name made lowercase.
    account = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    passwd = models.CharField(max_length=255)
    headpic = models.CharField(max_length=255, blank=True, null=True)
    facedata = models.CharField(max_length=255, blank=True, null=True)
    majorid = models.ForeignKey(Major, models.DO_NOTHING, db_column='majorId')  # Field name made lowercase.
    grade = models.IntegerField()
    email = models.CharField(max_length=255)
    intro = models.CharField(max_length=255)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'student'


class Teacher(models.Model):
    teacherid = models.AutoField(db_column='teacherId', primary_key=True)  # Field name made lowercase.
    account = models.CharField(max_length=255)
    pic = models.CharField(max_length=255)
    passwd = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    intro = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    majorid = models.ForeignKey(Major, models.DO_NOTHING, db_column='majorId')  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teacher'


class Teacherclass(models.Model):
    teacherclassid = models.AutoField(db_column='teacherclassId', primary_key=True)  # Field name made lowercase.
    teacherid = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='teacherId', blank=True, null=True)  # Field name made lowercase.
    classid = models.ForeignKey(Class, models.DO_NOTHING, db_column='classId', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teacherclass'


class Teachercourse(models.Model):
    teachercourseid = models.AutoField(db_column='teachercourseId', primary_key=True)  # Field name made lowercase.
    teacherid = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='teacherId')  # Field name made lowercase.
    courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='courseId')  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teachercourse'


class Weather(models.Model):
    weatherid = models.AutoField(db_column='weatherId', primary_key=True)  # Field name made lowercase.
    date = models.CharField(max_length=255)
    temp = models.CharField(max_length=255)
    intro = models.CharField(max_length=255, blank=True, null=True)
    pm = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weather'
