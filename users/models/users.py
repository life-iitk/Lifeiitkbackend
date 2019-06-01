from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField

class User(models.Model):
    roll = models.CharField(maxlength = 10, primary_key=True, unique=True)
    username = models.CharField(maxlength = 10)
    name = models.CharField(maxlength = 100)
    program=models.CharField(maxlength = 20)
    dept = models.CharField(maxlength = 50)
    hall = models.CharField(maxlength = 15)
    room = models.CharField(maxlength = 20)
    blood_group = models.CharField(maxlength = 4)
    gender = models.CharField(maxlength = 10)
    hometown = models.CharField(maxlength = 100)
    fblink = models.URLField(maxlength = 120)
    por = JSONField()
    earlier_login = models.BooleanField()
