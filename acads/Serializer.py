from rest_framework import serializers
from .models import AcadsModel
from tags.Serializer import TagSerializer

class AcadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcadsModel
        fields = (
            "course_id",
            "name",
            "code",
        )
