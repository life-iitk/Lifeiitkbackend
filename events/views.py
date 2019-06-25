from rest_framework.generics import RetrieveAPIView, ListAPIView

from .models import EventModel
from .Serializer import EventSerializer
from rest_framework.decorators import api_view

from datetime import date
today = date.today()

class SingleEventView(RetrieveAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer

class MonthEventView(ListAPIView):
    serializer_class = EventSerializer
    
    def get_queryset(self):
        query_month = self.request.data.get("month")
        if (query_month is not None):
            return EventModel.objects.filter(date__month=query_month).order_by("date", "time")
        return EventModel.objects.all()

class VenueEventView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        query_venue = self.request.data.get("venue")
        if (query_venue is not None):
            return EventModel.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day, venue=query_venue).order_by("time")
        return EventModel.objects.all()
