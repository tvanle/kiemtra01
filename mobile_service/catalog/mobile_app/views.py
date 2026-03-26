from rest_framework import viewsets, filters
from .models import Mobile
from .serializers import MobileSerializer

class MobileViewSet(viewsets.ModelViewSet):
    queryset = Mobile.objects.all()
    serializer_class = MobileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'brand']
