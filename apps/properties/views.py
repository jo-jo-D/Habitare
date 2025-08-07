from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

from apps.properties.models import Property, Amenities


class ListPropertiesView(ListAPIView):
    queryset = Property.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = []


class ListAmenities(ListAPIView):
    queryset = Amenities.objects.all()
    permission_classes = [AllowAny]
    serializer_class = []