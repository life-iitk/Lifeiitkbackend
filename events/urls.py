from django.urls import path
from .views import SingleEventView, MonthEventView, VenueEventView, FeedEventView, Feed_MonthEventView, CreateEventAPI

urlpatterns = [
    path("month/<int:pk>", SingleEventView.as_view()),
    path("view/venue/", VenueEventView.as_view()),
    path("view/month/", MonthEventView.as_view()),
    path("feed", FeedEventView.as_view()),
    path("feed/month/", Feed_MonthEventView.as_view()),
    path("", CreateEventAPI)
]
