from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from acads.models import AcadsModel
from tags.models import TagModel
import string
import random
import secrets

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
    password = models.CharField(max_length=70, null=True, blank=True)
    activated = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=70, blank=True, null=True)

    def generate_verification_code(self):
        """Generates verification code of length 28 made of digits and uppercase letters"""
        generated = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(28))
        self.verification_code = generated
        self.save()
        return self.verification_code
