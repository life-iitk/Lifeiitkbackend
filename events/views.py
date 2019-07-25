from rest_framework.generics import ListAPIView,CreateAPIView
from .models import EventModel
from .Serializer import EventSerializer
from rest_framework.decorators import api_view
from users.utils import IsLoggedIn
from tags.models import TagModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date
from rest_framework import status
from django.db.models import Q
import datetime
import re

today = date.today()
now = datetime.datetime.now()

def sorteventid(val):
    return val[0]


class MonthEventView(ListAPIView):
    serializer_class = EventSerializer
    
    def get_queryset(self):
        query_month = self.request.GET.get("month")
        query_year = today.year
        query_year = self.request.GET.get("year")
        if (query_month is not None and query_year is not None):
            EventList = EventModel.objects.filter(acad_state=False,date__year=query_year, date__month=query_month).order_by("date", "start_time")
            return EventList
        return Response(status = status.HTTP_400_BAD_REQUEST)

class VenueEventView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        query_venue = self.request.GET.get("venue")
        if (query_venue is not None):
            return EventModel.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day, venue_id=query_venue).order_by("start_time")
        return Response(status = status.HTTP_400_BAD_REQUEST)

class FeedEventView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        user = IsLoggedIn(self.request)
        if user is not None:
            tags = user.tags.all()
            tag_ids = [o.tag_id for o in tags]
            events = EventModel.objects.all()
            event_ids = list()
            for objects in events:
                event_tags = objects.tags.all()
                for tags in event_tags:
                    if tags.tag_id in tag_ids:
                        event_ids.append(objects.event_id)
            return EventModel.objects.filter(event_id__in=event_ids).order_by("date__year", "date__month", "date__day", "start_time")
        return EventModel.objects.all().order_by("date__year", "date__month", "date__day", "start_time")

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
            return EventModel.objects.filter(event_id__in=event_ids, date__year=query_year, date__month=query_month).order_by("date", "start_time")
        return None

class TagEventView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        get_query_tag = self.request.GET.get("tag_name")
        query_tag = TagModel.objects.filter(name=get_query_tag)
        #print(query_tag)
        if query_tag.exists():
            tag = query_tag[0]
            eventList = (
                EventModel.objects.filter(tags=tag)
                .filter(Q(date=now.date()) | Q(date__gt=now.date()))
                .order_by("-date")
            )

            return eventList
        return None

class AcadsEventView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        query_month = self.request.GET.get("month")
        query_year = self.request.GET.get("year")
        user = IsLoggedIn(self.request)
        if user is not None:
            user_acads = user.acads.all()
            course_id = [ course.code for course in user_acads ]

            eventList = EventModel.objects.filter(event_id=None)

            for acad_event in user_acads:
                eventList = eventList | acad_event.events.all()

            return eventList.filter(date__year=query_year,date__month=query_month).order_by("date", "start_time")
        return None

class CalenderAPI(ListAPIView):
    serializer_class = EventSerializer
    
    def get_queryset(self):
        query_month = self.request.GET.get("month")
        query_year = self.request.GET.get("year")
        user = IsLoggedIn(self.request)
        if user is not None:
            user_acads = user.acads.all()
            course_id = [ course.code for course in user_acads ]

            eventList = EventModel.objects.filter(event_id=None)

            print(query_month,query_year)
            for acad_event in user_acads:
                eventList = eventList | acad_event.events.all()

            non_academic_events = EventModel.objects.filter(acad_state=False)

            eventList = eventList | non_academic_events

            return eventList.filter(date__year=query_year,date__month=query_month).order_by("date", "start_time")
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def CreateEventAPI(request):
    if request.method == "POST":
        user = IsLoggedIn(request)
        if user is not None:
            owned_tags = user.owned.all()
            title = request.data.get("title")
            description = request.data.get("description")
            date_str = request.data.get("date")
            match = re.search(r'\d{4}-\d{2}-\d{2}', date_str)
            date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
            start_time = request.data.get("start_time")
            end_time = request.data.get("end_time")
            day_long = request.data.get("day_long")
            summary = request.data.get("summary")
            venue = request.data.get("venue")
            venue_id = request.data.get("venue_id")
            tag_name = request.data.get("tag_name")
            hash_tags = request.data.get("hash_tags")
            eventlist = EventModel.objects.all().order_by("event_id")
            tags = TagModel.objects.filter(name=tag_name)
            if len(tags) == 1:
                if tags[0] in owned_tags:
                    if len(eventlist) == 0:
                        event_id = 0
                    else:
                        event_id = eventlist.reverse()[0].event_id
                    data = EventModel(
                        event_id=event_id + 1,
                        title=title,
                        description=description,
                        date=date,
                        start_time=start_time,
                        end_time=end_time,
                        day_long=day_long,
                        summary=summary,
                        venue=venue,
                        venue_id=venue_id,
                        hash_tags=hash_tags,
                    )
                    data.save()
                    data.tags.add(tags[0])
                    data.save()
                    return Response(status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def DeleteEventAPI(request):
    if request.method == "DELETE":
        event_id = request.data.get("event_id")
        event = EventModel.objects.filter(event_id=event_id)
        if event.exists():
            event[0].delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
