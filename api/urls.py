from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import MyTokenObtainPairView, UserViewSet
from django.urls import path

from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename="users")


urlpatterns = [
    path('auth', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = router.urls
