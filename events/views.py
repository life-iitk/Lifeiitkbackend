from rest_framework.generics import RetrieveAPIView, ListAPIView

from .models import EventModel
from .Serializer import EventSerializer
from rest_framework.decorators import api_view
from users.utils import IsLoggedIn

from datetime import date
today = date.today()

class SingleEventView(RetrieveAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer

class MonthEventView(ListAPIView):
    serializer_class = EventSerializer
    
    def get_queryset(self):
        query_month = self.request.GET.get("month")
        query_year = today.year
        query_year = self.request.GET.get("year")
        if (query_month is not None and query_year is not None):
            return EventModel.objects.filter(date__year=query_year, date__month=query_month).order_by("date", "time")
        return EventModel.objects.all()

class VenueEventView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        query_venue = self.request.GET.get("venue")
        if (query_venue is not None):
            return EventModel.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day, venue=query_venue).order_by("time")
        return EventModel.objects.all()

class FeedEventView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        user = IsLoggedIn(self.request)
        if user is not None:
            print(EventModel.objects.all()[0].tags, EventModel.objects.all()[1].tags)
            tags = user.tags.all()
            tag_ids = [o.tag_id for o in tags]
            events = EventModel.objects.all()
            event_ids = list()
            for objects in events:
                event_tags = objects.tags.all()
                for tags in event_tags:
                    if tags.tag_id in tag_ids:
                        event_ids.append(objects.event_id)
            return EventModel.objects.filter(event_id__in=event_ids).order_by("date__year", "date__month", "date__day", "time")
        return None

class Feed_MonthEventView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        user = IsLoggedIn(self.request)
        if user is not None:
            print(EventModel.objects.all()[0].tags, EventModel.objects.all()[1].tags)
            tags = user.tags.all()
            tag_ids = [o.tag_id for o in tags]
            events = EventModel.objects.all()
            event_ids = list()
            for objects in events:
                event_tags = objects.tags.all()
                for tags in event_tags:
                    if tags.tag_id in tag_ids:
                        event_ids.append(objects.event_id)
            return EventModel.objects.filter(event_id__in=event_ids, date__year=today.year, date__month=today.month).order_by("date", "time")
        return None
