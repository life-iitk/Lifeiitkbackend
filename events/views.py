from rest_framework.generics import RetrieveAPIView

from .models import EventModel
from .Serializer import EventSerializer

class SingleEventView(RetrieveAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer

