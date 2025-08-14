from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookPropertyView, MyBookingsView, BookingsOfLandlord

router = DefaultRouter()
router.register('my-bookings', MyBookingsView, basename='my-bookings')
router.register('hosted', BookingsOfLandlord, basename='my-booked-properties')

urlpatterns = [
    path('', include(router.urls)),
    path('new/', BookPropertyView.as_view(), name='create-booking-of-property'),
    # path('hosted/', BookingsOfLandlord.as_view(), name='hosted-bookings'),
]