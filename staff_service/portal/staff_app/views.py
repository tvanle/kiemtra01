import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import login_required

@permission_classes([AllowAny])
def staff_login_page(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('staff_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            django_login(request, user)
            return redirect('staff_dashboard')
        return render(request, 'staff/login.html', {'error': 'Invalid Credentials or not staff'})
    return render(request, 'staff/login.html')

@login_required(login_url='/api/staff/')
def staff_dashboard_page(request):
    if not request.user.is_staff:
        return redirect('staff_login_page')
    return render(request, 'staff/dashboard.html')

def staff_logout(request):
    django_logout(request)
    return redirect('staff_login_page')

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None and user.is_staff:
        return Response({'message': 'Staff login successful', 'user_id': user.id, 'username': user.username})
    return Response({'error': 'Invalid Credentials or not staff'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_products(request):
    try:
        laptop_res = requests.get('http://laptop_service:8000/api/laptops/', headers={'Host': 'localhost'}, timeout=5)
        laptops = laptop_res.json() if laptop_res.status_code == 200 else []
    except:
        laptops = []
    try:
        clothes_res = requests.get('http://clothes_service:8000/api/clothes/', headers={'Host': 'localhost'}, timeout=5)
        clothes = clothes_res.json() if clothes_res.status_code == 200 else []
    except:
        clothes = []
    return Response({'laptops': laptops, 'clothes': clothes})

@api_view(['POST'])
@permission_classes([AllowAny])
def create_product(request):
    prod_type = request.data.get('type')
    payload = {k: v for k, v in request.data.items() if k != 'type'}
    if prod_type == 'laptop':
        res = requests.post('http://laptop_service:8000/api/laptops/', headers={'Host': 'localhost'}, json=payload, timeout=5)
    elif prod_type == 'clothes':
        res = requests.post('http://clothes_service:8000/api/clothes/', headers={'Host': 'localhost'}, json=payload, timeout=5)
    else:
        return Response({'error': 'Invalid product type'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        return Response(res.json(), status=res.status_code)
    except:
        return Response({'error': res.text}, status=res.status_code)

@api_view(['PUT'])
@permission_classes([AllowAny])
def update_product(request, pk):
    prod_type = request.data.get('type')
    payload = {k: v for k, v in request.data.items() if k != 'type'}
    if prod_type == 'laptop':
        res = requests.put(f'http://laptop_service:8000/api/laptops/{pk}/', headers={'Host': 'localhost'}, json=payload, timeout=5)
    elif prod_type == 'clothes':
        res = requests.put(f'http://clothes_service:8000/api/clothes/{pk}/', headers={'Host': 'localhost'}, json=payload, timeout=5)
    else:
        return Response({'error': 'Invalid product type'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        return Response(res.json(), status=res.status_code)
    except:
        return Response({'error': res.text}, status=res.status_code)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_product(request, pk):
    prod_type = request.query_params.get('type')
    if prod_type == 'laptop':
        res = requests.delete(f'http://laptop_service:8000/api/laptops/{pk}/', headers={'Host': 'localhost'}, timeout=5)
    elif prod_type == 'clothes':
        res = requests.delete(f'http://clothes_service:8000/api/clothes/{pk}/', headers={'Host': 'localhost'}, timeout=5)
    else:
        return Response({'error': 'Invalid product type'}, status=status.HTTP_400_BAD_REQUEST)
    if res.status_code == 204:
        return Response(status=status.HTTP_204_NO_CONTENT)
    try:
        return Response(res.json(), status=res.status_code)
    except:
        return Response({'error': res.text}, status=res.status_code)
