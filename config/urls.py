from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import MyTokenObtainPairView, UserViewSet, CustomTokenRefreshView
from django.urls import path

from rest_framework import routers
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('api.urls')),
    path('admin/', admin.site.urls),
    path('auth', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    
]
