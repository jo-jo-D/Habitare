from django.test import TestCase
from django.utils import timezone
from apps.accounts.models import User
from phonenumber_field.phonenumber import PhoneNumber
from django.core.exceptions import ValidationError


class UserModelTest(TestCase):
    def test_create_user_with_required_fields(self):
        user = User.objects.create(
            first_name="Jojo",
            last_name="Rabbit",
            email="jojo@example.com"
        )
        self.assertEqual(user.first_name, "Jojo")
        self.assertEqual(user.last_name, "Rabbit")
        self.assertEqual(user.email, "jojo@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.can_host)

    def test_get_full_name(self):
        user = User(first_name="Jojo", last_name="Rabbit", email="jr@example.com")
        self.assertEqual(user.get_full_name(), "Jojo Rabbit")

    def test_get_short_name(self):
        user = User(first_name="Jojo", last_name="Rabbit", email="jr@example.com")
        self.assertEqual(user.get_short_name(), "Jojo")

    def test_required_fields_validation(self):
        user = User(
            email=None,
            first_name="",
            last_name="",
        )
        with self.assertRaises(ValidationError):
            user.full_clean()


from django.core.exceptions import ValidationError
from django.test import TestCase
from apps.accounts.models import User


class UserPhoneValidationTest(TestCase):
    def test_invalid_phone_letters(self):
        user = User(
            first_name="Jojo",
            last_name="Rabbit",
            email="jojo_letters@example.com",
            phone="abc123"
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_invalid_phone_double_plus(self):
        user = User(
            first_name="Jojo",
            last_name="Rabbit",
            email="jojo_plus@example.com",
            phone="++49 123456789"
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_invalid_phone_too_short(self):
        user = User(
            first_name="Jojo",
            last_name="Rabbit",
            email="jojo_short@example.com",
            phone="12345"
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_valid_phone_formatted(self):
        user = User(
            first_name="Jojo",
            last_name="Rabbit",
            email="jojo_valid@example.com",
            phone="+49 15123456789",
            password="user123"
        )
        user.full_clean()
        user.save()
        self.assertEqual(user.phone.as_e164, "+4915123456789")

    def test_user_phone_number_parsing(self):
        user = User.objects.create(
            first_name="Jojo",
            last_name="Rabbit",
            email="jojo2@example.com",
            phone="+49 1234567890"
        )
        self.assertIsInstance(user.phone, PhoneNumber)
        self.assertEqual(user.phone.as_e164, "+491234567890")

