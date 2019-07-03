from django.urls import path
from .views import TagView

urlpatterns = [
    path("all/", TagView.as_view())
]
