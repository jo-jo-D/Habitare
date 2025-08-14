from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from apps.bookings.permissions import IsOwner
from apps.properties.models import Property
from apps.bookings.models import Booking
from apps.bookings.serializers import CreateBookingSerializer, ListBookingsSerializer, ListHostedBookingsView
from apps.properties.permissions import IsOwnerOrCreateOnly


class BookPropertyView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateBookingSerializer

    # def get_property(self):
    #     return get_object_or_404(Property, pk=self.kwargs['pk'])
    #
    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['booked_property'] = self.get_property()
    #     return context


class MyBookingsView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ListBookingsSerializer
    http_method_names = ['get', 'delete']

    def get_queryset(self):
        queryset =  Booking.all_objects.filter(tenant=self.request.user)
        status_of_booking = self.request.query_params.get('status')

        if status_of_booking == 'past':
            queryset = queryset.filter(end_date__lt=timezone.now()).filter(is_deleted=False)
        elif status_of_booking == 'active':
            queryset = queryset.filter(end_date__gte=timezone.now()).filter(is_deleted=False)
        elif status_of_booking == 'cancelled':
            queryset = queryset.filter(is_deleted=True)
        return queryset

    def destroy(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=self.kwargs['pk'], tenant=self.request.user)
        booking.delete()       # method of Booking model for "soft deletion"
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        booking = self.get_object()

        if booking.tenant != request.user:
            return Response({"detail": "You cannot cancel this booking."}, status=status.HTTP_403_FORBIDDEN)

        try:
            booking.cancel()
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "Booking has been cancelled."}, status=status.HTTP_200_OK)

class BookingsOfLandlord(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    # потом добавить сигнал пользователю о подтверждении или отклонении запроса на бронь
    permission_classes = [IsOwner]
    serializer_class = ListHostedBookingsView

    @action(methods=['patch'], detail=True)
    def decline(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.decline()   # метод из модели
        return Response(data={"status": "Booking has been declined."},
                        status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    def approve(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.approve()   # метод из модели
        return Response(data={"status": "Booking is approved!"},
                        status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Booking.all_objects.filter(booked_property__owner=self.request.user) # manager for viewing deleted obj
        status_of_booking = self.request.query_params.get('status')

        if status_of_booking == 'past':
            queryset = queryset.filter(end_date__lt=timezone.now()).filter(is_deleted=False)
        elif status_of_booking == 'active':
            queryset = queryset.filter(end_date__gte=timezone.now()).filter(is_deleted=False)
        elif status_of_booking == 'cancelled':
            queryset = queryset.filter(is_deleted=True)

        return queryset


