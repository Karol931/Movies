from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from movies_backend.utils import get_request_data_error_property, get_serializer_error_property, get_header_param
from movies_backend.exceptions import RequestDataException
# Create your views here.

@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
        }
),
responses={
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Succesfuly logged in.'),
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='token number'),
                'user': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                    'password': openapi.Schema(type=openapi.TYPE_STRING, description='hashed password')
                })
            },
    ),
    400: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'serializer': get_serializer_error_property(),
            'request data': get_request_data_error_property(),
        },
        description='Bad request error details'
    ),
})
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username= request.data.get('username')
    password= request.data.get('password')
    
    if not username and not password:
        raise RequestDataException
    
    data = {
        'username': username,
        'password': password,
    }
    context = {
        'request': request
    }

    serializer = LoginSerializer(data=data, context=context)

    if  serializer.is_valid():
        user = User.objects.get(username=request.data.get('username'))
        token, _ = Token.objects.get_or_create(user=user)
    else:
        return Response(status=400, data={'serializer': serializer.errors})
    print(serializer.data)
    return Response(status=200, data={'message': 'Succesfuly logged in.', 'token': token.key, 'user': serializer.data})
    

@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            'password_confirmation': openapi.Schema(type=openapi.TYPE_STRING, description='confirm your password'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
            'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is created user admin')
        }
),
responses={
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Succesfuly created account.'),
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='token number'),
                'user': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                    'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is user admin')
                })
            },
    ),
    400: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'serializer': get_serializer_error_property(),
            'request data': get_request_data_error_property(),
        },
        description='Bad request error details'
    ),
})
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    if not request.data:

        raise RequestDataException
    
    context = {'password_confirmation': request.data.pop('password_confirmation')}
    serializer = RegisterSerializer(data=request.data, context=context)
    
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data.get('username'))
        token = Token.objects.create(user=user)
    else:
        return Response(status=400, data={'errors': serializer.errors})
    
    return Response(status=200, data={'message': 'Succesfuly created account.', 'token': token.key, 'user': serializer.data})

@swagger_auto_schema(method='get',
manual_parameters=get_header_param(),
responses={
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='passed for \'email\'')
            },
    ),
    403: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Invalid token.'),
            'deatail': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication credentials were not provided.')
        },
        description='Error: Forbiden'
    )},
)
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response(status= 200, data={'token': f'Passed for {request.user.email}'})