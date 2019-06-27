from rest_framework import serializers
from .models import EventModel
from tags.Serializer import TagSerializer
from acads.Serializer import AcadsSerializer

class EventSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    acads = AcadsSerializer(read_only =True, many=True)
    class Meta:
        model = EventModel
        fields = (
            "event_id",
            "title",
            "description",
            "date",
            "start_time",
            "end_time",
            "venue",
            "venue_id",
            "tags",
            "acads",
            "day_long",
            "summary",
            "acads_state"
        )
