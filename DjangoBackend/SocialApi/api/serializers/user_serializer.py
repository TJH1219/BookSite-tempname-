from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.models import UserProfile

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'profile_image', ]

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'email_verified', 'first_name', 'last_name', 'profile']
        read_only_fields = ['email_verified']

        def update(self, instance, validated_data):
            profile_data = validated_data.pop('profile', None)
            user = super().update(instance, validated_data)

            if profile_data:
                profile_instance = getattr(user, 'profile', None)
                if not profile_instance:
                    profile_instance = UserProfile.objects.create(user=user)
                for attr , value in profile_data.items():
                    setattr(profile_instance, attr, value)
                profile_instance.save()
            return user