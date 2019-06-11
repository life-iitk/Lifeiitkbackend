from django.db import models
from tags.models import TagModel

# Create your models here.
class EventModel(models.Model):
    event_id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=20)
    venue_id = models.IntegerField()
    tags = models.ManyToManyField(TagModel)
