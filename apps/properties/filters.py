from rest_framework import filters


import django_filters
from django.db.models import Q, Count
from .models import Property, Amenities


class PropertyFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='Search')
    available_dates = django_filters.CharFilter(method='filter_by_dates', label='Available Dates')
    city = django_filters.CharFilter(
        field_name='address__city__name', lookup_expr='icontains', label='City name')
    country = django_filters.CharFilter(
        field_name='address__country__name', lookup_expr='icontains', label='Country name')
    amenities = django_filters.ModelMultipleChoiceFilter(
        field_name='amenities', queryset=Amenities.objects.all(), conjoined=True, label='Amenities')




    class Meta:
        model = Property
        fields = {
            'cost': ['lte', 'gte'],
            'rooms': ['exact', 'gte', 'lte'],
            'max_guests': ['exact', 'gte', 'lte'],
            'square_meters': ['exact','gte', 'lte'],
            'property_type': ['exact'],
            'rental_type': ['exact']
        }

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value)
        ).filter(approved=True)

    def filter_by_dates(self, queryset):
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')

        if start_date and end_date:
            queryset = queryset.exclude(
                bookings__start_date__lt=end_date,
                bookings__end_date__gt=start_date,
                bookings__approved=True
            )
        return queryset

    # def filter_by_amenities(self, queryset, name, value):
    #     amenities = self.data.getlist('amenities')  # list of ids
    #     if amenities:
    #         queryset = queryset.annotate(
    #             matched_amenities=Count(
    #                 'amenities',
    #                 filter=Q(amenities__id__in=amenities),
    #                 distinct=True
    #             )
    #         ).filter(matched_amenities=len(amenities))
    #     return queryset


