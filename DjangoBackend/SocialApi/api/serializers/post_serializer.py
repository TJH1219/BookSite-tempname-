from rest_framework import serializers
from rest_framework.response import Response

from api.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']

    def create(self, validated_data):
        post = Post(validated_data)
        post.save()

        return{
            "message": "Post Created",
            "post": {
                "id": post.id,
                "user": post.author.id,
                "title": post.title,
                "content": post.content,
                'created_at': post.created_at,
                'updated_at': post.updated_at
            }
        }

    def to_representation(self, instance):
        return{
            "message": "Post Retrieved",
            "post": {
                "id": instance.id,
                "user": instance.author.id,
                "title": instance.title,
                "content": instance.content,
                'created_at': instance.created_at,
                'updated_at': instance.updated_at
            }
        }