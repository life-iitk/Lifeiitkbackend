from rest_framework.generics import ListAPIView
from .models import AcadsModel
from .Serializer import AcadsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class AcadsView(ListAPIView):
    serializer_class = AcadsSerializer

    def get_queryset(self):
        acads = AcadsModel.objects.all()
        if acads.exists():
            return acads
        return None


# Create your views here.
