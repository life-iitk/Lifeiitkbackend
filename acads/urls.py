from django.urls import path
from .views import AcadsView

urlpatterns = [path("all/", AcadsView.as_view())]
