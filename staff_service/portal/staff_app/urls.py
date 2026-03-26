from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_login_page, name='staff_login_page'),
    path('dashboard/', views.staff_dashboard_page, name='staff_dashboard'),
    path('logout/', views.staff_logout, name='staff_logout'),
    path('api/login/', views.login, name='staff_login'),
    path('api/products/', views.list_products, name='list_products'),
    path('api/product/create/', views.create_product, name='create_product'),
    path('api/product/<int:pk>/update/', views.update_product, name='update_product'),
    path('api/product/<int:pk>/delete/', views.delete_product, name='delete_product'),
]
