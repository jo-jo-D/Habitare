from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _


User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,validators=[validate_password])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    can_host = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = [
                    'first_name', 'last_name', 'email', 'password',
                    'date_of_birth', 'gender', 'can_host',
                    'phone', 'passport', 'bank_iban']


    def validate(self, attrs):
        can_host = attrs.get('can_host')
        if can_host:
            host_required_fields = ['phone', 'first_name', 'last_name', 'passport', 'bank_iban']
            for field in host_required_fields:
                required_value = attrs.get(field, getattr(self.instance, field, None))
                if not required_value:
                    raise serializers.ValidationError({field: _('This field is required for hosts.')})

        return attrs

    def validate_password(self, value):
        if not self.instance and not value:
            raise serializers.ValidationError(_("Password can't be empty."))
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    # def validate_password(self, value):
    #     if not value:
    #         raise serializers.ValidationError(_("Password can't be empty."))
    #     return value


class ProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    can_host = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password',
            'date_of_birth', 'gender', 'can_host',
            'phone', 'passport', 'bank_iban'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'phone': {'required': False, 'allow_null': True},
            'passport': {'required': False},
            'bank_iban': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'date_of_birth': {'required': False},
            'gender': {'required': False},
        }

    def validate(self, attrs):
        can_host = attrs.get('can_host', getattr(self.instance, 'can_host', False))
        if can_host:
            host_required_fields = ['phone', 'first_name', 'last_name', 'passport', 'bank_iban']
            for field in host_required_fields:
                value = attrs.get(field, getattr(self.instance, field, None))
                if not value or (isinstance(value, str) and not value.strip()):
                    raise serializers.ValidationError({field: _('This field is required for hosts.')})
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        # Обработка пустых значений для unique-полей
        if 'phone' in validated_data and validated_data['phone'] == '':
            validated_data['phone'] = None

        # Обновляем только переданные поля
        for attr, value in validated_data.items():
            if value is not None and value != '':
                setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
