from rest_framework import serializers
from .models import Property, Amenities
from ..locations.models import City, Country, Address
from ..locations.serializers import AddressSerializer, CitySerializer, CountrySerializer


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = ['id', 'name']


class PropertyListingSerializer(serializers.ModelSerializer):       #while search not all fields are needed
    """For the view of search and filter by any user, essential info only"""
    class Meta:                                                     # in view filter/search
        model = Property
        fields = ['name', 'cost', 'property_type', 'square_meters', 'max_guests' ]  #add city address etc


class PropertyDetailedViewSerializer(serializers.ModelSerializer):
    city = CitySerializer(source='address.city',read_only=True)
    country = CountrySerializer(source='address.country',read_only=True)    #might duplicate country field from city
    address = AddressSerializer( read_only=True)
    amenities = AmenitiesSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            'name', 'description', 'cost', 'rental_type', 'property_type',
            'square_meters', 'rooms', 'bathrooms', 'max_guests',
            'average_rating', 'reviews_count',
            'city', 'country', 'address', 'amenities',
            'created_at'
        ]

class MainPropertySerializer(serializers.ModelSerializer):
    street = serializers.CharField(write_only=True, max_length=255)
    house_number = serializers.CharField(write_only=True, max_length=30)
    apartment_number = serializers.CharField(write_only=True, required=False, allow_blank=True)
    # эти поля добавляем для их появления для заполнения формы, они отправятся заполнить форму по своим моделям и исчезнут
    # для создания принимает только ID города.
    city = serializers.PrimaryKeyRelatedField(  # и проверяет существует ли такой ID в queryset всех городов
        queryset=City.objects.all(),
        write_only=True,
        label="City ID"
    )
    amenities = serializers.PrimaryKeyRelatedField(
        queryset = Amenities.objects.all(),
        write_only=True,
        many=True,
        label="Amenities ID"
    )

    address = AddressSerializer(read_only=True)
    amenities_info = AmenitiesSerializer(source="amenities", many=True, read_only=True)
    city_data = serializers.PrimaryKeyRelatedField(source='city.name', read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'name', 'description', 'cost', 'rental_type', 'property_type',
            'square_meters', 'rooms', 'bathrooms', 'max_guests',
            'is_active', 'reviews_count', 'average_rating',
            'amenities', 'amenities_info',
            'street', 'house_number', 'apartment_number', 'city', 'city_data',
            'address', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reviews_count', 'average_rating', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Redefining standart method create to customize creation of two connected models
        """
        address_data = {
            'street': validated_data.pop('street'),
            'house_number': validated_data.pop('house_number'),
            'apartment_number': validated_data.pop('apartment_number'),
            'city': validated_data.pop('city'),
        }
        address = Address.objects.create(**address_data)
        amenities = validated_data.pop('amenities', [])
        print(self.context['request'].user)

        property_instance = Property.objects.create(address=address, owner=self.context['request'].user,
                                                     **validated_data)
        property_instance.amenities.set(amenities)
        return property_instance

    def update(self, instance, validated_data):
        amenities = validated_data.pop('amenities', None)
        address_data = {
            'street': validated_data.pop('street', instance.address.street),
            'house_number': validated_data.pop('house_number', instance.address.house_number),
            'apartment_number': validated_data.pop('apartment_number', instance.address.apartment_number),
            'city': validated_data.pop('city', instance.address.city)
        }
        Address.objects.filter(id=instance.address.id).update(**address_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if amenities is not None:
            instance.amenities.set(amenities)

        instance.save()
        return instance