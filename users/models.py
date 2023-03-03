"""
Model for User Profile and image
"""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    A database for user's profile and their image
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='profile_images', null=True, blank=True
    )

    def __str__(self):
        """
        Show User's profile name
        """
        return f'{self.user.username} Profile'
