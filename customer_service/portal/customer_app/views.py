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
        laptop_res = requests.get(f'http://api_gateway/api/laptop/laptops/?search={query}', timeout=3)
        laptops = laptop_res.json() if laptop_res.status_code == 200 else []
    except:
        laptops = []
        
    try:
        mobile_res = requests.get(f'http://api_gateway/api/mobile/mobiles/?search={query}', timeout=3)
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
