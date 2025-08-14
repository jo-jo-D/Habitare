from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from .models import Review
from .serializers import ReviewCreateSerializer, ReviewListSerializer, ReviewDetailSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    GET /reviews/ — list
    POST /reviews/ — creation
    GET /property/<pk>/reviews/ — all reviews for the property
    GET /property/<pk>/reviews/<pk> — detailed review
    PUT/PATCH /reviews/<pk>/ — update
    DELETE /reviews/<pk>/ — deletion
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """ Getting all reviews for chosen property"""
        return Review.objects.filter(property_id_id=self.kwargs['property_pk']).select_related('reviewer', 'property_id')

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewListSerializer
        elif self.action == 'retrieve':
            return ReviewDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ReviewCreateSerializer
        return ReviewDetailSerializer

    def perform_create(self, serializer):
        serializer.save(
            reviewer=self.request.user,
            property_id_id=self.kwargs['property_pk']
        )




