from django.db import models

# Create your models here.
class AcadsModel(models.Model):
	course_id = models.IntegerField(primary_key=True, unique=True)
	name=models.CharField(max_length=40) 
	code=models.CharField(max_length=8)
	venue=models.CharField(max_length=5)   #TB111
	venue_id = models.IntegerField()
