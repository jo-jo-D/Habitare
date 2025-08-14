from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ReviewViewSet
from ..properties.views import PropertyFilterListingView
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()

router.register(r'property', PropertyFilterListingView)
# router.register(r'reviews', ReviewViewSet, basename='reviews')

properties_router = NestedDefaultRouter(router, r'property', lookup='property')
properties_router.register(r'reviews', ReviewViewSet, basename='property-reviews')



urlpatterns = [
    path('', include(router.urls)),
    path('', include(properties_router.urls)),
    # path('properties/<int:property_id>/reviews/', PropertyReviewsViewSet.as_view(), name='property-reviews'),
]
