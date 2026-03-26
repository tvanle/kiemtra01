from django.urls import path
from . import views

urlpatterns = [
    # Template routes (no prefix)
    path('', views.customer_login_page, name='customer_login_page'),
    path('login/', views.customer_login_page, name='customer_login'),
    path('register/', views.customer_register_page, name='customer_register'),
    path('dashboard/', views.customer_dashboard_page, name='customer_dashboard'),
    path('logout/', views.customer_logout, name='customer_logout'),
    # API routes (prefixed with api/)
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login, name='api_login'),
    path('api/search/', views.search_products, name='search'),
]
