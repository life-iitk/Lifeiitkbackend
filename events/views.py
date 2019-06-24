from rest_framework.generics import RetrieveAPIView, ListAPIView

from .models import EventModel
from .Serializer import EventSerializer

class SingleEventView(RetrieveAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer

class MonthEventView(ListAPIView):
    serializer_class = EventSerializer
    
    def get_queryset(self):
        query_month = self.request.GET.get("month")
        if(query_month is not None):
            return EventModel.objects.filter(date__month=query_month).order_by("date", "time")
        return EventModel.objects.all()
