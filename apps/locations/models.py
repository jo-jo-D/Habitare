from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    """
        Country storage model.
    """
    name = models.CharField(max_length=255, unique=True, db_index=True, verbose_name=_("Country Name"))
    iso2 = models.CharField(max_length=2, unique=True, db_index=True,
                            verbose_name=_("Two-letter country codes as per ISO 3166-1 alpha-2."))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = ["name"]


class City(models.Model):
    """
            City storage model.
    """
    zip_code = models.CharField(max_length=10,  db_index=True, verbose_name=_("Zip Code"))
    name = models.CharField(max_length=255, db_index=True, verbose_name=_("City Name"))
    latitude = models.FloatField(verbose_name=_("latitude"))
    longitude = models.FloatField(verbose_name=_("longitude"))
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name=_("Country"))


    def __str__(self):
        return f"{self.name}, {self.country.name}"

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        unique_together = ('name', 'country', 'zip_code')
        ordering = ['country', 'name']


class Address(models.Model):
    street = models.CharField(max_length=255, db_index=True, verbose_name=_("Street"))
    house_number = models.CharField(max_length=255,  verbose_name=_("House number"))
    apartment_number = models.CharField(max_length=255, verbose_name=_("Apartment/block number"), null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name=_("City"), related_name="addresses")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name=_("Country"), related_name="addresses")

    def __str__(self):
        # Формируем строку адреса из существующих полей
        address_parts = [
            self.street,
            self.house_number,
            str(self.city)
        ]
        if self.apartment_number:
            address_parts.append(f"apt {self.apartment_number}")

        return ", ".join(filter(None, address_parts))

    @property
    def country(self):
        """
        Удобное свойство для прямого доступа к стране через город.
        Использование: my_address.country
        """
        return self.city.country

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        # Исправленный ordering. Используем двойное подчеркивание для доступа к полям связанных моделей.
        ordering = ["city__country__name", "city__name", "street", "house_number", "apartment_number"]
        # Добавляем ограничение, чтобы не было дубликатов адресов
        unique_together = ('city', 'street', 'house_number', 'apartment_number')


