"""
URL configuration for SocialApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

import api
from api.token_management import CustomTokenRefreshView
from api.views.auth_views import AuthViewSet
from api.views.user_views import UserViewSet
from api.views.db_reset import ResetViewSet

router = DefaultRouter()
router.register('auth', AuthViewSet, basename='auth')
router.register('users', UserViewSet, basename='users')
router.register('api', ResetViewSet, basename='reset')


urlpatterns = [
    *router.urls,
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh')
]
