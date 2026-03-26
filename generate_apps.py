import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + '\n')

# LAPTOP
write_file("laptop_service/catalog/laptop_app/models.py", """
from django.db import models

class Laptop(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    cpu = models.CharField(max_length=100, blank=True, null=True)
    ram = models.CharField(max_length=50, blank=True, null=True)
    storage = models.CharField(max_length=50, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name
""")
write_file("laptop_service/catalog/laptop_app/serializers.py", """
from rest_framework import serializers
from .models import Laptop

class LaptopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laptop
        fields = '__all__'
""")
write_file("laptop_service/catalog/laptop_app/views.py", """
from rest_framework import viewsets
from .models import Laptop
from .serializers import LaptopSerializer

class LaptopViewSet(viewsets.ModelViewSet):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer
""")
write_file("laptop_service/catalog/laptop_app/urls.py", """
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'laptops', views.LaptopViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
""")

# MOBILE
write_file("mobile_service/catalog/mobile_app/models.py", """
from django.db import models

class Mobile(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    screen_size = models.CharField(max_length=50, blank=True, null=True)
    battery = models.CharField(max_length=50, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name
""")
write_file("mobile_service/catalog/mobile_app/serializers.py", """
from rest_framework import serializers
from .models import Mobile

class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = '__all__'
""")
write_file("mobile_service/catalog/mobile_app/views.py", """
from rest_framework import viewsets
from .models import Mobile
from .serializers import MobileSerializer

class MobileViewSet(viewsets.ModelViewSet):
    queryset = Mobile.objects.all()
    serializer_class = MobileSerializer
""")
write_file("mobile_service/catalog/mobile_app/urls.py", """
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'mobiles', views.MobileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
""")

# CUSTOMER
write_file("customer_service/portal/customer_app/models.py", """
from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_id = models.IntegerField()
    product_type = models.CharField(max_length=50) # 'laptop' or 'mobile'
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
""")
write_file("customer_service/portal/customer_app/serializers.py", """
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cart, CartItem

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
""")
write_file("customer_service/portal/customer_app/views.py", """
import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from .models import Cart, CartItem
from .serializers import UserSerializer, CartSerializer, CartItemSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        Cart.objects.create(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        django_login(request, user)
        return Response({'message': 'Login successful', 'user_id': user.id})
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def search_products(request):
    query = request.query_params.get('q', '')
    
    # Calls to other services (through gateway ideally, but direct internal network is faster here)
    try:
        laptop_res = requests.get(f'http://api_gateway:8000/api/laptop/laptops/?search={query}', timeout=3)
        laptops = laptop_res.json() if laptop_res.status_code == 200 else []
    except:
        laptops = []
        
    try:
        mobile_res = requests.get(f'http://api_gateway:8000/api/mobile/mobiles/?search={query}', timeout=3)
        mobiles = mobile_res.json() if mobile_res.status_code == 200 else []
    except:
        mobiles = []

    return Response({
        'laptops': laptops,
        'mobiles': mobiles
    })

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
""")
write_file("customer_service/portal/customer_app/urls.py", """
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'carts', views.CartViewSet)
router.register(r'cart-items', views.CartItemViewSet)

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('search/', views.search_products, name='search'),
    path('', include(router.urls)),
]
""")

# STAFF
write_file("staff_service/portal/staff_app/views.py", """
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None and user.is_staff:
        return Response({'message': 'Staff login successful', 'user_id': user.id})
    return Response({'error': 'Invalid Credentials or not staff'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_product(request):
    # Proxy to correct service
    prod_type = request.data.get('type') # 'laptop' or 'mobile'
    if prod_type == 'laptop':
        res = requests.post('http://api_gateway:8000/api/laptop/laptops/', json=request.data, timeout=5)
        return Response(res.json(), status=res.status_code)
    elif prod_type == 'mobile':
        res = requests.post('http://api_gateway:8000/api/mobile/mobiles/', json=request.data, timeout=5)
        return Response(res.json(), status=res.status_code)
    return Response({'error': 'Invalid product type'}, status=status.HTTP_400_BAD_REQUEST)
""")
write_file("staff_service/portal/staff_app/urls.py", """
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='staff_login'),
    path('product/create/', views.create_product, name='create_product'),
]
""")

print("Apps generated successfully.")
