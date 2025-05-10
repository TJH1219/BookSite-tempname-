from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsOwnerOrAdmin
from api.serializers.user_serializer import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('profile').all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return self.queryset
        return self.queryset.filter(id=user.id)