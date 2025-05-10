from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers.user_serializer import UserSerializer

User = get_user_model()

class RegisterSerializer(ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirmed_password', 'access', 'refresh','first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmed_password']:
            raise serializers.ValidationError({"password" :"Passwords do not match"})
        validate_password(attrs['password'], self.instance)
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirmed_password', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        refresh = RefreshToken.for_user(user)
        return{
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

    def to_representation(self, instance):
        return {
            'user' : instance['user'],
            'access': instance['access'],
            'refresh': instance['refresh']
        }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Must include username and password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User is not active")

        refresh = RefreshToken.for_user(user)
        attrs['user'] = user
        attrs['access'] = str(refresh.access_token)
        attrs['refresh'] = str(refresh)

        return attrs

    def to_representation(self, instance):
        user = instance['user']
        access = instance['access']
        refresh = instance['refresh']
        user_data = UserSerializer(user).data
        return {
            'user' : {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'access': access,
            'refresh': refresh
        }