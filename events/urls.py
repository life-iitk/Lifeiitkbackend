from django.urls import path
from .views import SingleEventView, MonthEventView, VenueEventView

urlpatterns = [
    path("month/<int:pk>", SingleEventView.as_view()),
    path("view/venue/", VenueEventView.as_view()),
    path("view/month/", MonthEventView.as_view()),
]
