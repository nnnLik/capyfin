from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserDetails


@receiver(post_save, sender=User)
def create_user_details(instance: User, created: bool, **_: dict) -> None:
    if created:
        UserDetails.objects.get_or_create(user_id=instance.id)
