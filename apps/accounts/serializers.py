from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'date_of_birth', 'gender']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        print(email, password)

        user = authenticate(username=email, password=password)
        print(user)

        if not user:
            raise AuthenticationFailed('Invalid credentials')

        data['user'] = user
        return data



# class HostSignUpSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True)
#     email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'password', 'date_of_birth', 'gender', 'passport', ]

# class HostSerializer(serializers.ModelSerializer):
