from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _


User = get_user_model()

# class SignUpOrEditProfileSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
#     can_host = serializers.BooleanField(required=False, default=False)
#
#
#     class Meta:
#         model = User
#         fields = [
#             'first_name', 'last_name', 'email', 'password',
#             'date_of_birth', 'gender', 'can_host',
#
#             'phone', 'passport', 'bank_iban',
#         ]
#         extra_kwargs = {
#             'phone': {'required': False},
#             'passport': {'required': False},
#             'bank_iban': {'required': False},
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance:
#             self.fields['password'].required = False
#             for field in ['first_name', 'last_name', 'email', 'date_of_birth', 'gender']:
#                 self.fields[field].required = False
#
#
#     def validate(self, attrs):
#         can_host = attrs.get('can_host', getattr(self.instance, 'can_host', False))
#         if can_host:
#             host_required_fields = ['phone', 'first_name', 'last_name', 'passport', 'bank_iban']
#             for field in host_required_fields:
#                 required_value = attrs.get(field, getattr(self.instance, field, None))
#                 if not required_value:
#                     raise serializers.ValidationError({field: _('This field is required for hosts.')})
#
#         return attrs
#
#     def validate_password(self, value):
#         if not self.instance and not value:
#             raise serializers.ValidationError(_("Password can't be empty."))
#         return value
#
#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)
#
#     def update(self, instance, validated_data):
#         password = validated_data.pop('password', None)
#         for attr, value in validated_data.items():
#             if value is not None and value != '':
#                 setattr(instance, attr, value)
#
#         if password:
#             instance.set_password(password)
#
#         instance.save()
#         return instance


class SignUpOrEditProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    can_host = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password',
            'date_of_birth', 'gender', 'can_host',
            'phone', 'passport', 'bank_iban',
        ]
        extra_kwargs = {
            'phone': {'required': False, 'allow_null': True},
            'passport': {'required': False},
            'bank_iban': {'required': False},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['password'].required = False
            for field in ['first_name', 'last_name', 'email', 'date_of_birth', 'gender']:
                self.fields[field].required = False

    def validate(self, attrs):
        can_host = attrs.get('can_host', getattr(self.instance, 'can_host', False))
        if can_host:
            host_required_fields = ['phone', 'first_name', 'last_name', 'passport', 'bank_iban']
            for field in host_required_fields:
                value = attrs.get(field, getattr(self.instance, field, None))
                if not value or (isinstance(value, str) and not value.strip()):
                    raise serializers.ValidationError({field: _('This field is required for hosts.')})
        return attrs

    def validate_password(self, value):
        if not self.instance and not value:
            raise serializers.ValidationError(_("Password can't be empty."))
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        # Специальная обработка для phone: если '' , установить None
        if 'phone' in validated_data and validated_data['phone'] == '':
            validated_data['phone'] = None

        # Обновляем только непустые поля
        for attr, value in validated_data.items():
            if value is not None and value != '':
                setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

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
            raise AuthenticationFailed(_('Invalid credentials'))

        data['user'] = user
        return data




