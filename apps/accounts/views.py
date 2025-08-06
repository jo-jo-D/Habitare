from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.serializers import SignUpSerializer, User, LoginSerializer


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

# class HostSignUpView(CreateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = HostSignUpSerializer

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
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            response = Response(data={
                "user": {"user": user.first_name + " " + user.last_name, "email": user.email},
                "details": "Sign up successful!"},
                 status=status.HTTP_201_CREATED)
            set_jwt_cookies(response, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(data={"details":"Logout successful!"}, status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(key='access_token')
        response.delete_cookie(key='refresh_token')
        return response


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello, {request.user.first_name}! This is a protected view."})

