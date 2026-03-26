from rest_framework import viewsets, filters
from .models import Laptop
from .serializers import LaptopSerializer

class LaptopViewSet(viewsets.ModelViewSet):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'brand']
