from django.db import models

# Create your models here.
class TagModel(models.Model):
    tag_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length = 40)
    description = models.CharField(max_length = 100,blank=True, default="")
