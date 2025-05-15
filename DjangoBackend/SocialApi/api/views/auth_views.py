from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers.auth_serializers import RegisterSerializer, LoginSerializer
from api.serializers.user_serializer import UserSerializer


class AuthViewSet(viewsets.GenericViewSet):
    def get_serializer_class(self):
        if self.action == 'register':
            return RegisterSerializer
        elif self.action == 'login':
            return LoginSerializer
        elif self.action == 'logout':
            return LoginSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['register', 'login']:
            self.permission_classes = [AllowAny]
        elif self.action in ['logout']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                result = serializer.save()
            except IntegrityError:
                return Response(
                    {
                        "success": False,
                        "errors": "Username or email taken."
                     },
                    status = status.HTTP_409_CONFLICT
                )
            return Response(
                {
                    "success": True,
                    "message": "User registered successfully.",
                    **serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response({"success": False, "errors": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {
                    "success": True,
                    "message": "User logged in successfully.",
                    **serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            errors = serializer.errors
            invalid_credentials = 'Invalid Credentials.' in str(errors)
            return Response(
                {"success": False, "errors": errors},
                status=status.HTTP_401_UNAUTHORIZED if invalid_credentials else status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['post'], detail=False)
    def logout(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {"success": False, "errors": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"success": True, "message": "User logged out successfully."},
                status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {"success": False, "errors": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )

