from django.urls import path
from .views import *

urlpatterns = [
    path('amenities/', ListAmenities.as_view(), name='amenities'),

]