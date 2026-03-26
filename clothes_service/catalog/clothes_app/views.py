from rest_framework import viewsets, filters
from .models import Clothes
from .serializers import ClothesSerializer

class ClothesViewSet(viewsets.ModelViewSet):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'brand']
