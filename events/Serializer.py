from rest_framework import serializers
from .models import EventModel
from tags.Serializer import TagSerializer

class EventSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    class Meta:
        model = EventModel
        fields = (
            "event_id",
            "title",
            "description",
            "date",
            "time",
            "venue",
            "venue_id",
            "tags"
        )
