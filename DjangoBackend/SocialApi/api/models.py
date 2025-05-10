from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    dob = models.DateField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='api_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )


    def has_role(self, role_name : str) -> bool:
        return self.roles.filter(name=role_name).exists()

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)

class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    permissions = models.ManyToManyField(Permission, blank=True,related_name='roles')
    users = models.ManyToManyField('User', blank=True, related_name='roles')

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()

class Friends(models.Model):
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user2')