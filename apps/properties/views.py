from pickle import FALSE

from django.db.models import Q
from django.db.models.aggregates import Count
from rest_framework.filters import OrderingFilter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.mixins import UpdateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend


from apps.properties.models import Property, Amenities
from apps.properties.serializers import AmenitiesSerializer, PropertyListingSerializer, \
    MainPropertySerializer, PropertyDetailedViewSerializer
from .filters import PropertyFilter
from .permissions import  IsOwnerOrCreateOnly
from ..bookings.serializers import CreateBookingSerializer


class PropertyFilterListingView(ModelViewSet):
    """Filtered, sorted search, listing of all available properties"""
    queryset = Property.objects.all()
    serializer_class = PropertyListingSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PropertyFilter
    ordering_fields = ['cost', 'rooms', 'max_guests', 'square_meters', 'average_rating']
    ordering = ['cost']

    def get_serializer_class(self):
        if self.action == 'list':
            return PropertyListingSerializer
        elif self.action == 'retrieve':
            return PropertyDetailedViewSerializer
        return PropertyListingSerializer

    # @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    """ пока создаем букинг через домашнюю модель localhost/bookings/new/ """
    # def book(self, request, pk=None):
    #     property_instance = self.get_object()
    #
    #     serializer = CreateBookingSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     booking = serializer.save(booked_property=property_instance, tenant=request.user)
    #
    #     return Response(CreateBookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class ListAmenities(ListCreateAPIView):
    """View for admin to view List of available Amenities or add new ones"""
    queryset = Amenities.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = AmenitiesSerializer

class ManageMyPropertiesView(ModelViewSet):
    """
    Available for hosts only.
    Get, create, update, activate, deactivate, delete your posted properties
    """
    serializer_class = MainPropertySerializer
    permission_classes = [IsOwnerOrCreateOnly]

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, *args, **kwargs):
        property = self.get_object()
        property.is_active = False
        property.save()
        return Response(data={"status": "Property is deactivated and no longer displayed in search."},
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def activate(self, request, *args, **kwargs):
        property = self.get_object()
        property.is_active = True
        property.save()
        return Response(data={"status": "Property is activated and available to book now."}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"status": "Property is created", "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )



# class ManageMyPropertiesView(ListCreateAPIView):
#     serializer_class = MainPropertySerializer
#     permission_classes = [IsOwnerOrCreateOnly]
#
#     def get_queryset(self):
#         return Property.objects.filter(owner=self.request.user)
#
#     def perform_create(self, serializer):
#         serializer.save()






