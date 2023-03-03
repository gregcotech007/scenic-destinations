"""
Add Profile to Admin Panel
"""
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
