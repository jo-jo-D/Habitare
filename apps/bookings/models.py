from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.properties.models import Property
from utils.managers import ActiveManager

User = get_user_model()

class Booking(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
                               related_name='bookings', verbose_name=_('Your bookings') )
    booked_property = models.ForeignKey(Property, on_delete=models.CASCADE, null=False, blank=False,
                                related_name= 'bookings', verbose_name=_("Your stay at: ") )
    start_date = models.DateField(null=False, blank=False, verbose_name=_("Check-in"))
    end_date = models.DateField(null=False, blank=False, verbose_name=_("Check-out"))
    total_price_brutto = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                         verbose_name=_("Total price taxes incl.") )
    total_price_netto = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                         verbose_name=_("Price for your stay"))
    city_taxes = models.DecimalField(max_digits=4, decimal_places=2, null=True, verbose_name=_("Lodging tax"))
    amount_of_guests = models.PositiveIntegerField(null=False, blank=False, verbose_name=_("Amount of guests"),
                                                 validators=[MinValueValidator(0), MaxValueValidator(30)])
    is_deleted = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    all_objects = models.Manager()
    objects = ActiveManager()

    CANCELLATION_DEADLINE_DAYS = 3  #

    def __str__(self):
        start_str = self.start_date.strftime('%d %B')
        end_str = self.end_date.strftime('%d %B')
        return _(f"Booking #{id} at {self.booked_property.name},  {start_str} - {end_str}")

    @property
    def count_amount_of_nights(self):
        return Decimal((self.end_date - self.start_date).days)

    @property
    def get_booking_date_frames(self):
        return self.start_date, self.end_date

    def delete(self, using=None, keep_parents=False):   # безполезно, убрать позже
        """Complete deletion of the booking if it was cancelled before."""
        if self.is_deleted == True:
            super(Booking, self).delete(using=using, keep_parents=keep_parents)
        else:
            raise ValidationError(_("This booking cannot be deleted."))

    def approve(self):
        self.approved = True
        self.save(update_fields=['approved'])

    def decline(self):
        self.approved = False
        self.save(update_fields=['approved'])

    def can_be_cancelled(self):
        """Check if this booking can be cancelled."""
        deadline = self.start_date - timedelta(days=self.CANCELLATION_DEADLINE_DAYS)
        return timezone.now().date() <= deadline

    def cancel(self):
        """Cancell booking if still possible."""
        if not self.can_be_cancelled():
            raise ValidationError(
                f"Cancellation can be made no later than {self.CANCELLATION_DEADLINE_DAYS} day(s) before check-in")
        self.is_deleted = True
        self.save()

    def save(self, **kwargs):
        if self.booked_property and self.start_date and self.end_date:
            nights = self.count_amount_of_nights
            nightly_cost = self.booked_property.cost

            self.total_price_netto = nightly_cost * nights
            self.city_taxes = (self.total_price_netto * Decimal('0.05')).quantize(Decimal('0.01'))
            self.total_price_brutto = self.total_price_netto + self.city_taxes

        super().save(**kwargs)



