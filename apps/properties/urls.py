from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('manage', ManageMyPropertiesView, basename='my-properties')
router.register('listing', PropertyFilterListingView, basename='listing-properties')


urlpatterns = [
    path('', include(router.urls)),
    # path('my/', ManageMyPropertiesView.as_view(), name='manage-properties'),
    path('amenities/', ListAmenities.as_view(), name='list amenities')

]