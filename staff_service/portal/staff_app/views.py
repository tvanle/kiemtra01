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
        res = requests.post('http://api_gateway/api/laptop/laptops/', json=request.data, timeout=5)
        return Response(res.json(), status=res.status_code)
    elif prod_type == 'mobile':
        res = requests.post('http://api_gateway/api/mobile/mobiles/', json=request.data, timeout=5)
        return Response(res.json(), status=res.status_code)
    return Response({'error': 'Invalid product type'}, status=status.HTTP_400_BAD_REQUEST)
