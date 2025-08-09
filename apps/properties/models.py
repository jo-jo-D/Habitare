from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from django.utils.translation import gettext_lazy as _

# from apps.reviews.models import Review

User = get_user_model()

PROPERTY_TYPE_CHOICES = [
    ('apartment', _('Apartment')),
    ('studio', _('Studio')),
    ('house', _('House')),
    ('townhouse', _('Townhouse')),
    ('room', _('Room')),
    ('loft', _('Loft')),
    ('duplex', _('Duplex')),
    ('penthouse', _('Penthouse')),
    ('bungalow', _('Bungalow')),
    ('cottage', _('Cottage')),
    ('office', _('Office')),
    ('retail', _('Retail space')),
    ('warehouse', _('Warehouse')),
    ('other', _('Other')),
]
RENTAL_TYPE_CHOICES = [('daily', _('Daily')),
                       ('monthly', _('Monthly'))]

class Property(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"), validators=[MinLengthValidator(5)],
                            blank=False, null=False, unique=True, db_index=True)
    description = models.TextField(verbose_name=_("Description"))
    cost = models.DecimalField(max_digits=10, decimal_places=2, db_index=True,
                                         verbose_name=_("Price"), blank=False, null=False)
    rental_type = models.CharField(choices=RENTAL_TYPE_CHOICES, max_length=25, blank=False, null=False,)
    property_type = models.CharField(choices=PROPERTY_TYPE_CHOICES, max_length=25, verbose_name=_("Property type"),
                                    blank=False, null=False, db_index=True)
    square_meters = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    amenities = models.ManyToManyField('Amenities', related_name='properties', verbose_name=_("Amenities of the property"))
    bedrooms = models.IntegerField(verbose_name=_("Bedrooms"), blank=True, null=True, db_index=True)
    bathrooms = models.IntegerField(verbose_name=_("Bathrooms"), blank=True, null=True)
    # address = models.ForeignKey('locations.Location', on_delete=models.PROTECT)
    max_guests = models.IntegerField(verbose_name=_("Guests"), blank=True, null=True, db_index=True)
    owner = models.ForeignKey(User, verbose_name=_("Owner"), on_delete=models.CASCADE, related_name="properties")
    is_active = models.BooleanField(verbose_name=_("Is active"), default=True)
    available = models.BooleanField(verbose_name=_("Available"), default=True)

    reviews_count = models.PositiveIntegerField(default=0, verbose_name=_("Amount of reviews"))
    average_rating = models.DecimalField(max_digits=3,  decimal_places=1, default=0.0,  verbose_name=_("Average rating of the property"))

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")
        ordering = ['-created_at']





class Amenities(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Amenities"))
