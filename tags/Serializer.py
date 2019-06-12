from rest_framework import serializers
from .models import TagModel

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ('tag_id', 'name', 'description')