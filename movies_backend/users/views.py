from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    data = {
        'username': request.data.get('username'),
        'password': request.data.get('password'),
    }
    context = {'request': request}
    serializer = LoginSerializer(data=data, context=context)
    if  serializer.is_valid():
        user = User.objects.get(username=request.data.get('username'))
        token, _ = Token.objects.get_or_create(user=user)
        return Response(status=200, data={'message': 'Succesfuly logged in.', 'token': token.key, 'user': serializer.data})
    return Response(status=400, data={'errors': serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    context = {'password_confirmation': request.data.pop('password_confirmation')}
    serializer = RegisterSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data.get('username'))
        token = Token.objects.create(user=user)
    else:
        return Response(status=400, data={'errors': serializer.errors})
    
    return Response(status=200, data={'message': 'Succesfuly created account.', 'token': token.key, 'user': serializer.data})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response(f'Passed for {request.user.email}')