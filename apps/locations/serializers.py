from rest_framework import serializers
from .models import Address, City, Country
from django.utils.translation import gettext_lazy as _

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'iso2']  # Добавьте 'id' для уникальной идентификации

class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()  # Включаем страну для отображения
    class Meta:
        model = City
        fields = ['id', 'zip_code', 'name', 'country']  # Добавьте 'id' для уникальной идентификации

class AddressSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    country = serializers.SerializerMethodField()  # for seeing a country through

    class Meta:
        model = Address
        fields = ['street', 'house_number', 'apartment_number', 'city', 'country']

    def validate(self, attrs):
        # Проверяем полноту только если адрес используется (для хостов это будет проверено выше)
        if not attrs.get('street') or not attrs.get('house_number'):
            raise serializers.ValidationError(_('Street and house number are required for a valid address.'))
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance and instance.city:
            representation['city'] = f"{instance.city.name}, {instance.city.country.name}"
        else:
            representation['city'] = None
        return representation

    def get_country(self, obj):
        if obj.city and obj.city.country:
            return CountrySerializer(obj.city.country).data
        return None

    def create(self, validated_data):
        city_id = validated_data.pop('city')
        city = City.objects.get(id=city_id)
        address = Address.objects.create(city=city, **validated_data)
        return address

    def update(self, instance, validated_data):
        city_id = validated_data.pop('city', instance.city_id)
        if city_id:
            instance.city = City.objects.get(id=city_id)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance