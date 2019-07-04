from django.db import models

# Create your models here.
class AcadsModel(models.Model):
    course_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=8)
