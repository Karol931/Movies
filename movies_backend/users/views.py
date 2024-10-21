from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
# Create your views here.

@api_view(['POST'])
def login(request):
    data = {
        'username': request.data.get('username'),
        'password': request.data.get('password'),
    }
    context = {'request': request}
    serializer = LoginSerializer(data=data, context=context)
    if not serializer.is_valid():
        return Response(status=400, data={'errors': serializer.errors})
    
    return Response(status=200, data={'Succesfuly logged in.'})


@api_view(['POST'])
def register(request):
    data = {
        'username': request.data.get('username'),
        'email': request.data.get('email'),
        'password': request.data.get('password'),
        'is_staff': request.data.get('is_staff'),
    }
    context = {'password_confirmation': request.data.get('password_confirmation')}
    serializer = RegisterSerializer(data=data, context=context)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(status=400, data={'errors': serializer.errors})
    
    return Response(status=200, data={'Succesfuly created account.'})