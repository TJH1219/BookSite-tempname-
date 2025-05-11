from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models import Post
from api.permissions import IsOwnerOrAdmin
from api.serializers.post_serializer import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('profile').all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return self.queryset
        return self.queryset.filter(author=user.profile)