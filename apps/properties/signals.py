from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Property
from apps.reviews.models import Review



@receiver(post_save, sender=Review)
def review_saved(instance, **kwargs):
    update_propery_rating_count(instance.property_id)

@receiver(post_delete, sender=Review)
def review_deleted(instance, **kwargs):
    update_propery_rating_count(instance.property_id)

def update_propery_rating_count(property_obj):
    reviews = property_obj.reviews.all()
    amount_of_reviews = reviews.count()

    if amount_of_reviews > 0:
        rating_for_property = sum([review.average_rating for review in reviews]) / amount_of_reviews
    else:
        rating_for_property = 0.0

    property_obj.reviews_count = amount_of_reviews
    property_obj.average_rating = rating_for_property
    property_obj.save(update_fields=['reviews_count', 'average_rating'])
