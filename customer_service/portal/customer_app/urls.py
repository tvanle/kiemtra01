from django.urls import path
from . import views

urlpatterns = [
    # API routes - path starts with api/ because main urls.py has path('api/', ...)
    path('api/customer/register/', views.register),
    path('api/customer/login/', views.login),
    path('api/customer/search/', views.search_products),
    # Template routes
    path('', views.customer_login_page, name='customer_login_page'),
    path('login/', views.customer_login_page, name='customer_login'),
    path('register/', views.customer_register_page, name='customer_register'),
    path('dashboard/', views.customer_dashboard_page, name='customer_dashboard'),
    path('logout/', views.customer_logout, name='customer_logout'),
]
