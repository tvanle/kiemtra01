import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from .serializers import UserSerializer

@permission_classes([AllowAny])
def customer_login_page(request):
    if request.user.is_authenticated:
        return redirect('customer_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            django_login(request, user)
            return redirect('customer_dashboard')
        return render(request, 'customer/login.html', {'error': 'Invalid Credentials'})
    return render(request, 'customer/login.html')

@permission_classes([AllowAny])
def customer_register_page(request):
    if request.user.is_authenticated:
        return redirect('customer_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'customer/register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, email=email, password=password)
        requests.post('http://cart_service:8000/api/carts/', json={'user': user.id})
        django_login(request, user)
        return redirect('customer_dashboard')
    return render(request, 'customer/register.html')

@login_required(login_url='/api/customer/login/')
def customer_dashboard_page(request):
    return render(request, 'customer/dashboard.html', {'user': request.user})

def customer_logout(request):
    django_logout(request)
    return redirect('customer_login_page')

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        requests.post('http://cart_service:8000/api/carts/', json={'user': user.id})
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
    try:
        laptop_res = requests.get(f'http://laptop_service:8000/api/laptops/?search={query}', headers={'Host': 'localhost'}, timeout=3)
        laptops = laptop_res.json() if laptop_res.status_code == 200 else []
    except:
        laptops = []
    try:
        clothes_res = requests.get(f'http://clothes_service:8000/api/clothes/?search={query}', headers={'Host': 'localhost'}, timeout=3)
        clothes = clothes_res.json() if clothes_res.status_code == 200 else []
    except:
        clothes = []
    return Response({'laptops': laptops, 'clothes': clothes})

class CartViewSet(viewsets.ModelViewSet):
    queryset = None
    serializer_class = None

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = None
    serializer_class = None
