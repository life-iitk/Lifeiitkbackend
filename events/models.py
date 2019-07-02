from django.db import models
from tags.models import TagModel
from acads.models import AcadsModel
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class EventModel(models.Model):
    event_id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_long = models.BooleanField(default=False)
    summary = models.CharField(max_length=500,null=True)
    venue = models.CharField(max_length=20)
    venue_id = models.IntegerField()
    tags = models.ManyToManyField(TagModel)
    acads = models.ManyToManyField(AcadsModel)
    acad_state = models.BooleanField(default=False)
    hash_tags = ArrayField(models.CharField(max_length=40), blank=True)
