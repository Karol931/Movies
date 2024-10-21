from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'is_staff']

    def validate(self, attrs):
        print(attrs.get('password'), self.context.get('password_confirmation'))
        if attrs.get('password') != self.context.get('password_confirmation'):
            raise serializers.ValidationError({'password': 'Password fields didn\'t match.'})
        
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data.get('username'),
            email = validated_data.get('email'),
            is_staff = validated_data.get('is_staff')
        )

        user.set_password(validated_data.get('password'))
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, fields):
        username = fields.get('username')
        password = fields.get('password')
        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials', code='authorization')
        
        else:
            raise serializers.ValidationError('Must contain \'username\' and \'password\'.', code='authorization')
        
        return user
