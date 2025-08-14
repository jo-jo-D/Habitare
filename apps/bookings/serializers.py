from decimal import Decimal

from rest_framework import serializers
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from apps.bookings.models import Booking



class CreateBookingSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    amount_of_guests = serializers.IntegerField()

    class Meta:
        model = Booking
        fields = [
            'id', 'booked_property', 'tenant',
            'start_date', 'end_date',
            'amount_of_guests',
            'city_taxes', 'total_price_netto', 'total_price_brutto'
        ]
        read_only_fields = [ 'city_taxes', 'total_price_brutto', 'total_price_netto', 'tenant']

    def validate(self, attrs):
        start = attrs.get('start_date')
        end = attrs.get('end_date')

        if start >= end:
            raise serializers.ValidationError(_("Start date must be before the end date"))

        property_instance = attrs['booked_property']
        if property_instance.bookings.filter(
                start_date__lt=end,
                end_date__gt=start,
                is_deleted=False
        ).exists():
            raise serializers.ValidationError(_("These dates are already booked by someone else."))

        return attrs

    def create(self, validated_data):
        booking_start = validated_data.pop('start_date')
        booking_end = validated_data.pop('end_date')
        amount_of_guests = validated_data.pop('amount_of_guests')
        property_instance = validated_data.pop('booked_property')

        booking = Booking.objects.create(
            tenant=self.context['request'].user,
            start_date=booking_start,
            end_date=booking_end,
            booked_property=property_instance,
            amount_of_guests=amount_of_guests,
            **validated_data
        )

        price_per_night = booking.booked_property.cost
        nights_count = booking.count_amount_of_nights
        taxes = price_per_night * Decimal('0.05') * nights_count * amount_of_guests  # 5% с гостя
        booking.tax_amount = taxes
        booking.total_price_netto = price_per_night * nights_count * amount_of_guests
        booking.total_price_brutto = booking.total_price_netto + taxes
        booking.save()

        return booking


class ListBookingsSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source='booked_property.name', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'property_name', 'start_date', 'end_date', 'amount_of_guests', 'total_price_brutto']

class ListHostedBookingsView(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'