from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager


GENDER_CHOICES = {
    "f": "Female",
    "m": "Male",
    "o": "Other",
}
class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    first_name = models.CharField(_("first name"), max_length=150, blank=False, null=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False, null=False)
    phone = PhoneNumberField(region='DE', blank=True, null=True, unique=True)
    date_of_birth = models.DateField(_("date of birth"), blank=True, null=True)
    gender = models.CharField(_("gender"), choices=GENDER_CHOICES, max_length=1, blank=True, null=True)
    email = models.EmailField(_("email address"), blank=False, unique=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    can_host = models.BooleanField(default=False)
    # host_address = models.OneToOneField(Address, null=True, blank=True, on_delete=models.SET_NULL, related_name='host_user')
    # passport = models.CharField(blank=True, null=True, max_length=50)
    # address = models.CharField(blank=True, null=True, max_length=150)
    # bank_iban = models.CharField(blank=True, null=True, max_length=150)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name