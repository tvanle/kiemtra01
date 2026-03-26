from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='staff_login'),
    path('product/create/', views.create_product, name='create_product'),
]
