from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'clothes', views.ClothesViewSet)
router.register(r'mobiles', views.ClothesViewSet, basename='mobiles')

urlpatterns = [
    path('', include(router.urls)),
]
