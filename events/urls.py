from django.urls import path
from .views import MonthEventView, VenueEventView, FeedEventView, Feed_MonthEventView, CreateEventAPI, DeleteEventAPI, TagEventView, AcadsEventView, CalenderAPI

urlpatterns = [
    path("view/venue/", VenueEventView.as_view()),
    path("view/month/", MonthEventView.as_view()),
    path("feed/", FeedEventView.as_view()),
    path("feed/month/", Feed_MonthEventView.as_view()),
    path("view/tagged_events/", TagEventView.as_view()),
    path("create/", CreateEventAPI),
    path("delete/", DeleteEventAPI),
    path("acads/",AcadsEventView.as_view()),
    path("all/",CalenderAPI.as_view())
]
