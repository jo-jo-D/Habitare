from django.contrib import admin
from .models import Country, City, Address


admin.site.register(Country)
admin.site.register(City)
admin.site.register(Address)