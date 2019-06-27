from rest_framework.generics import RetrieveAPIView, ListAPIView,CreateAPIView
from .models import EventModel
from .Serializer import EventSerializer
from rest_framework.decorators import api_view
from users.utils import IsLoggedIn
from tags.models import TagModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date
from rest_framework import status


today = date.today()
def sorteventid(val):
    return val[0]

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
            query_month = self.request.GET.get("month")
            query_year = today.year
            query_year = self.request.GET.get("year")
            tags = user.tags.all()
            tag_ids = [o.tag_id for o in tags]
            events = EventModel.objects.all()
            event_ids = list()
            for objects in events:
                event_tags = objects.tags.all()
                for tags in event_tags:
                    if tags.tag_id in tag_ids:
                        event_ids.append(objects.event_id)
            return EventModel.objects.filter(event_id__in=event_ids, date__year=query_year, date__month=query_month).order_by("date", "time")
        return None

@api_view(['POST', ])
def CreateEventAPI(request):
    if request.method == 'POST':
        title = request.data.get("title")
        description = request.data.get("description")
        date = request.data.get("date")
        time = request.data.get("time")
        venue = request.data.get("venue")
        venue_id = request.data.get("venue_id")
        tags = request.data.get("tags")
        eventlist = EventModel.objects.all().order_by("event_id")
        event_id = eventlist.reverse()[0].event_id
        print(event_id)
        data = EventModel(
            event_id = event_id + 1,
            title = title,
            description= description,
            date = date,
            time= time,
            venue = venue,
            venue_id = venue_id
        )
        data.save()
        for tag in tags:
            tag_id = tag.get("tag_id")
            tag_row = TagModel.objects.get(tag_id = tag_id)
            data.tags.add(tag_row)
        data.save()
        return Response(status = status.HTTP_200_OK)
