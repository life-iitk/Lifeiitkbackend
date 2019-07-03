from rest_framework.generics import ListAPIView
from .Serializer import TagSerializer
from tags.models import TagModel

# Create your views here.

class TagView(ListAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        return TagModel.objects.all()
