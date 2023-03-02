"""
File for Blog App
"""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    Configuration for Blog App
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
