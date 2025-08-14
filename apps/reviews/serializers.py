from django.utils import timezone
from rest_framework import serializers
from .models import Review


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Creation of new review"""
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=1, read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'property_id', 'comment',
            'cleanliness', 'comfort_and_facilities', 'staff_communication',
            'localisation', 'value_for_money', 'wifi_connection',
            'average_rating'
        ]
        read_only_fields = ['id', 'average_rating']

    def validate(self, data):
        tenant = self.context['request'].user
        booked_propery = data['property_id']

        has_past_booking = booked_propery.bookings.filter(
            tenant=tenant,
            end_date__lt=timezone.now(),
            is_deleted=False,
            approved=True
        ).exists()

        if not has_past_booking:
            raise serializers.ValidationError("You can only leave a review for the accommodation you rented.")

        return data

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user

        review = super().create(validated_data)
        # моодель сама вызовет count_average_rating() в save()
        return review



class ReviewDetailSerializer(serializers.ModelSerializer):
    """Details of review (all fields)"""
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    property_name = serializers.CharField(source='property_id.name', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'property_id', 'property_name', 'reviewer', 'reviewer_name',
            'comment', 'created_at', 'updated_at',
            'average_rating', 'cleanliness', 'comfort_and_facilities',
            'staff_communication', 'localisation', 'value_for_money', 'wifi_connection'
        ]
        read_only_fields = fields


class ReviewListSerializer(serializers.ModelSerializer):
    """List of reviews, short notes"""
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    property_name = serializers.CharField(source='property_id.name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'property_name', 'reviewer_name', 'average_rating', 'comment', 'created_at']
