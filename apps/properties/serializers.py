from rest_framework import serializers
from .models import Property, Amenities


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = '__all__'


class ManageMyPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

