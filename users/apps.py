"""
File for App Configuration
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Import Signals
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
