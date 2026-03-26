from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='staff_login'),
    path('products/', views.list_products, name='list_products'),
    path('product/create/', views.create_product, name='create_product'),
    path('product/<int:pk>/update/', views.update_product, name='update_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
]
