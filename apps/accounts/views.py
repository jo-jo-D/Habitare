from django.contrib.auth import authenticate, logout
from django.shortcuts import render
from rest_framework import status, request
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from .serializ import SignUpSerializer, ProfileUpdateSerializer
from apps.accounts.serializers import User, LoginSerializer, SignUpOrEditProfileSerializer


def set_jwt_cookies(response, user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token

    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True, secure=False, samesite='Lax', path='/'
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True, secure=False, samesite='Lax', path='/'
    )


class LoginView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        response = Response(data={"detail": "Login successful"}, status=status.HTTP_200_OK)
        set_jwt_cookies(response, user)
        print(response.cookies)
        return response


class SignUpView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        response = Response(data={
            "user": {"user": user.first_name + " " + user.last_name,
                     "email": user.email},
            "details": "Sign up successful!"},
             status=status.HTTP_201_CREATED)
        set_jwt_cookies(response, user)
        return response


@permission_classes([AllowAny])
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        request.session.flush()         # удаляем  сессионные данные
        response = Response(data={"details": "Logout successful!"}, status=status.HTTP_200_OK)
        response.delete_cookie(key='access_token')
        response.delete_cookie(key='refresh_token')
        return response

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello, {request.user.first_name}! This is a protected view."})


class EditProfileView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileUpdateSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        print(f"Data received in perform_update: {self.request.data}")  # Отладка входных данных
        user = serializer.save()
        return Response({"user": {
             "full_name": f"{user.first_name} {user.last_name}",
                "email": user.email,
                "can_host": user.can_host
            },
            "details": "Profile updated successfully!"
        })





