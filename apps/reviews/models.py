from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from apps.properties.models import Property
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Review(models.Model):
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews', verbose_name=_("Property that was reviewed"))
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL ,related_name='reviews', verbose_name=_("ID of the reviewer"), null=True)
    comment = models.TextField(verbose_name=_("Comment"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    average_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0,
                                         verbose_name=_("Overall rating of the property"))
    cleanliness = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name=_("Cleanliness"))
    comfort_and_facilities = models.DecimalField(max_digits=3, default=0, decimal_places=0,
                                                 verbose_name=_("Comfort and facilities"))
    staff_communication = models.DecimalField(max_digits=3, decimal_places=0, default=0,
                                              verbose_name=_("Communication with staff"))
    localisation = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name=_("Localisation"))
    value_for_money = models.DecimalField(max_digits=3, decimal_places=0, default=0,
                                          verbose_name=_("Value for money"))
    wifi_connection = models.DecimalField(max_digits=3, decimal_places=0, default=0,
                                          verbose_name=_("Quality of Wi-Fi connection"))


    def count_average_rating(self):
        ratings = [self.cleanliness,
                   self.comfort_and_facilities,
                   self.staff_communication,
                   self.localisation,
                   self.value_for_money,
                   self.wifi_connection]
        total = sum(Decimal(str(rating)) for rating in ratings) # avg_rat по дефолту уже десимал, но укажу явно тип Decimal
        average = total / Decimal(str(len(ratings))) # юзеры могут ставить оценки только int, и что бы avg_rat(Decimal, 3, 1) не конфликовало с ним, нужно свести к одному типу данных
        return average.quantize(Decimal('0.1'))

    def save(self, *args, **kwargs):
        self.average_rating = self.count_average_rating()
        super().save(*args, **kwargs)

