from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from acads.models import AcadsModel
from tags.models import TagModel


class User(models.Model):
    roll = models.CharField(max_length=20, primary_key=True, unique=True)
    username = models.CharField(max_length=20)
    image = models.CharField(max_length=200,null=True, blank=True)
    name = models.CharField(max_length=100)
    program = models.CharField(max_length=20)
    dept = models.CharField(max_length=50)
    hall = models.CharField(max_length=15)
    room = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=14)
    gender = models.CharField(max_length=10)
    hometown = models.CharField(max_length=100)
    fblink = models.URLField(max_length=120, null=True)
    por = JSONField(default=dict, null=True)
    earlier_login = models.BooleanField(default=0, null=True)
    acads = models.ManyToManyField(AcadsModel)
    owned = models.ManyToManyField(TagModel, through="privilege.privileges",related_name="admins")
    tags = models.ManyToManyField(TagModel, related_name="tags")
