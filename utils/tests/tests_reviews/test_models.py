# import unittest
# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from apps.properties.models import Property
# from apps.reviews.models import Review
# from decimal import Decimal
# from django.utils import timezone
#
# User = get_user_model()
#
# class ReviewModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             first_name="Jojo",
#             last_name="Tester",
#             email='testuser@example.com',
#             password='testpass123'
#         )
#
#         self.property = Property.objects.create(
#             name='Test Property',
#             description='A test property',
#             cost=100.00,
#             square_meters=125.0,
#             rental_type="1",
#             property_type="2",
#             owner_id=self.user.id
#         )
#
#         self.review = Review.objects.create(
#             property_id=self.property,
#             reviewer=self.user,
#             comment='Great stay!',
#             cleanliness=Decimal('8'),  # Явно используем Decimal
#             comfort_and_facilities=Decimal('7'),
#             staff_communication=Decimal('9'),
#             localisation=Decimal('8'),
#             value_for_money=Decimal('7'),
#             wifi_connection=Decimal('6')
#         )
#         try:
#             self.review.save()
#             print("Review saved successfully:", Review.objects.filter(id=self.review.pk).exists())
#         except Exception as e:
#             print("Error saving review:", str(e))
#             raise
#
#     def test_review_creation(self):
#         """Test that a review is created with correct attributes."""
#         self.assertEqual(self.review.property_id, self.property)
#         self.assertEqual(self.review.reviewer, self.user)
#         self.assertEqual(self.review.comment, 'Great stay!')
#         self.assertEqual(self.review.cleanliness, Decimal('8'))
#         self.assertEqual(self.review.comfort_and_facilities, Decimal('7'))
#         self.assertEqual(self.review.staff_communication, Decimal('9'))
#         self.assertEqual(self.review.localisation, Decimal('8'))
#         self.assertEqual(self.review.value_for_money, Decimal('7'))
#         self.assertEqual(self.review.wifi_connection, Decimal('6'))
#         self.assertTrue(self.review.created_at <= timezone.now())
#         self.assertTrue(self.review.updated_at <= timezone.now())
#
#     def test_count_average_rating(self):
#         """Test the count_average_rating method."""
#         expected_average = (Decimal('8') + Decimal('7') + Decimal('9') +
#                            Decimal('8') + Decimal('7') + Decimal('6')) / Decimal('6')
#         expected_average = expected_average.quantize(Decimal('0.1'))
#         self.assertEqual(self.review.count_average_rating(), expected_average)
#
#     def test_save_updates_average_rating(self):
#         """Test that save method updates average_rating."""
#         self.review.cleanliness = Decimal('9')
#         self.review.comfort_and_facilities = Decimal('8')
#         self.review.save()
#
#         expected_average = (Decimal('9') + Decimal('8') + Decimal('9') +
#                            Decimal('8') + Decimal('7') + Decimal('6')) / Decimal('6')
#         expected_average = expected_average.quantize(Decimal('0.1'))
#         self.assertEqual(self.review.average_rating, expected_average)
#
#     def test_reviewer_null_on_user_deletion(self):
#         """Test that reviewer is set to NULL when user is deleted."""
#         self.user.delete()
#         self.review.refresh_from_db()
#         self.assertIsNone(self.review.reviewer)
#
#     def test_property_cascade_on_delete(self):
#         """Test that review is deleted when associated property is deleted."""
#         property_id = self.review.property_id.id
#         self.property.delete()
#         self.assertFalse(Review.objects.filter(id=self.review.pk).exists())
#
#     def test_field_verbose_names(self):
#         """Test verbose names of fields."""
#         field_verbose_names = {
#             'property_id': 'Property that was reviewed',
#             'reviewer': 'ID of the reviewer',
#             'comment': 'Comment',
#             'average_rating': 'Overall rating of the property',
#             'cleanliness': 'Cleanliness',
#             'comfort_and_facilities': 'Comfort and facilities',
#             'staff_communication': 'Communication with staff',
#             'localisation': 'Localisation',
#             'value_for_money': 'Value for money',
#             'wifi_connection': 'Quality of Wi-Fi connection'
#         }
#
#         for field_name, verbose_name in field_verbose_names.items():
#             field = Review._meta.get_field(field_name)
#             self.assertEqual(field.verbose_name, verbose_name)
#
#     def test_decimal_field_constraints(self):
#         """Test that decimal fields enforce max_digits and decimal_places."""
#         review = Review(
#             property_id=self.property,
#             reviewer=self.user,
#             comment='Test constraints'
#         )
#         review.cleanliness = Decimal('9999')
#         with self.assertRaises(Exception):
#             review.full_clean()
#
#         review.cleanliness = Decimal('9')
#         review.full_clean()
#
#     def test_default_values(self):
#         """Test default values for rating fields."""
#         review = Review.objects.create(
#             property_id=self.property,
#             reviewer=self.user,
#             comment='No ratings provided'
#         )
#         self.assertEqual(review.average_rating, Decimal('0.0'))
#         self.assertEqual(review.cleanliness, Decimal('0'))
#         self.assertEqual(review.comfort_and_facilities, Decimal('0'))
#         self.assertEqual(review.staff_communication, Decimal('0'))
#         self.assertEqual(review.localisation, Decimal('0'))
#         self.assertEqual(review.value_for_money, Decimal('0'))
#         self.assertEqual(review.wifi_connection, Decimal('0'))
#
# if __name__ == '__main__':
#     unittest.main()