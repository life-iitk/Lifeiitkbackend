from django.urls import path
from .views import SingleEventView, MonthEventView

urlpatterns = [
    path("<int:pk>", SingleEventView.as_view()),
    path("", MonthEventView.as_view()),
]
