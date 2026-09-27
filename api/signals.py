import secrets

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Company


@receiver(post_save, sender=User)
def create_company_profile(sender, instance, created, **kwargs):
    """
    Fires whenever a User is saved. On first creation (created=True),
    auto-create the linked Company profile and generate a unique api_key.
    """
    if created:
        Company.objects.create(
            user=instance,
            company_name=instance.email,
            api_key=secrets.token_urlsafe(32),
        )
