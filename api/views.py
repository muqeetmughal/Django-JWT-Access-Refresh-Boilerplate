import json
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # you need to instantiate the serializer with the request data
        serializer = self.serializer_class(data=request.data)
        # you must call .is_valid() before accessing validated_data
        serializer.is_valid(raise_exception=True)

        # get access and refresh tokens to do what you like with
        access = serializer.validated_data.get("access", None)
        refresh = serializer.validated_data.get("refresh", None)
        user = serializer.validated_data.get("user", None)

        # build your response and set cookie
        if access is not None:
            response = Response(
                {"access": access, "refresh": refresh, "user": user}, status=200)
            response.set_cookie('refresh', refresh, httponly=True)
            return response

        return Response({"Error": "Something went wrong"}, status=400)


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_uid = decoded_payload['user_id']
        print(data)
        # add filter query
        # data.update({'custom_field': 'custom_data')})
        return data


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom Refresh token View
    """
    serializer_class = CustomTokenRefreshSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
