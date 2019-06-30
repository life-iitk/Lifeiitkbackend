from rest_framework import serializers
from .models import User
from tags.Serializer import TagSerializer
from acads.Serializer import AcadsSerializer

class UserSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    acads = AcadsSerializer(read_only=True, many=True)
    owned = TagSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = (
            "roll",
            "username",
            "image",
            "name",
            "program",
            "dept",
            "hall",
            "room",
            "blood_group",
            "gender",
            "hometown",
            "fblink",
            "por",
            "earlier_login",
            "tags",
            "acads",
            "owned"
        )
class UserOwnedSerializer(serializers.ModelSerializer):
    owned = TagSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = (
            "roll",
            "owned"
        )

class UserAcadsSerializer(serializers.ModelSerializer):
    acads = AcadsSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = (
            "roll",
            "acads"
        )
