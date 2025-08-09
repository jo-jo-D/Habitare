from django.db.models import Q
from django.db.models.aggregates import Count
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.mixins import UpdateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.properties.models import Property, Amenities
from apps.properties.serializers import AmenitiesSerializer, ManageMyPropertiesSerializer
from .permissions import IsOwner


class ListPropertiesView(ListAPIView):
    queryset = Property.objects.all()
    permission_classes = [AllowAny]
    # serializer_class = #cделать сериалайзер для фильтрации

    def get_queryset(self):
        queryset = super().get_queryset()
        amenities_params = queryset.get_params.get_list('amenities')

        if amenities_params:
            queryset = queryset.annotate(
            matched_amenities=Count('amenities', filter=Q(amenities__id__in=amenities_params), distinct=True))

        return queryset


class ListAmenities(ListAPIView):
    queryset = Amenities.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AmenitiesSerializer

class ManageMyPropertiesView(ModelViewSet):
    serializer_class= ManageMyPropertiesSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(['post'], detail=True)
    def deactivate(self, request, *args, **kwargs):
        property = request.get_object()
        property.is_active = False
        property.save()
        return Response(data={"status": "Property is deactivated"}, status=status.HTTP_200_OK)
