from django.urls import path
from .views import SingleEventView

urlpatterns = [
    path("<int:pk>", SingleEventView.as_view())
]