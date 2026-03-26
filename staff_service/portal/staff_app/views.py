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
        return Response({'message': 'Staff login successful', 'user_id': user.id, 'username': user.username})
    return Response({'error': 'Invalid Credentials or not staff'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_products(request):
    """List all laptops and mobiles"""
    try:
        laptop_res = requests.get('http://laptop_service:8000/api/laptops/', headers={'Host': 'localhost'}, timeout=5)
        laptops = laptop_res.json() if laptop_res.status_code == 200 else []
    except:
        laptops = []
    try:
        mobile_res = requests.get('http://mobile_service:8000/api/mobiles/', headers={'Host': 'localhost'}, timeout=5)
        mobiles = mobile_res.json() if mobile_res.status_code == 200 else []
    except:
        mobiles = []
    return Response({'laptops': laptops, 'mobiles': mobiles})

@api_view(['POST'])
@permission_classes([AllowAny])
def create_product(request):
    prod_type = request.data.get('type')
    payload = {k: v for k, v in request.data.items() if k != 'type'}
    if prod_type == 'laptop':
        res = requests.post('http://laptop_service:8000/api/laptops/', headers={'Host': 'localhost'}, json=payload, timeout=5)
    elif prod_type == 'mobile':
        res = requests.post('http://mobile_service:8000/api/mobiles/', headers={'Host': 'localhost'}, json=payload, timeout=5)
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
    elif prod_type == 'mobile':
        res = requests.put(f'http://mobile_service:8000/api/mobiles/{pk}/', headers={'Host': 'localhost'}, json=payload, timeout=5)
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
    elif prod_type == 'mobile':
        res = requests.delete(f'http://mobile_service:8000/api/mobiles/{pk}/', headers={'Host': 'localhost'}, timeout=5)
    else:
        return Response({'error': 'Invalid product type'}, status=status.HTTP_400_BAD_REQUEST)
    if res.status_code == 204:
        return Response(status=status.HTTP_204_NO_CONTENT)
    try:
        return Response(res.json(), status=res.status_code)
    except:
        return Response({'error': res.text}, status=res.status_code)
