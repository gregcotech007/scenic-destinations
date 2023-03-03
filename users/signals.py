"""
File to listen for User's send and receive signals
"""
from django.db.models.signals import post_save
from django.contrib.auth.models import User  # Sender
from django.dispatch import receiver  # Receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Send a signal when a profile is created
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Receive a signal when a profile is created
    """
    instance.profile.save()
