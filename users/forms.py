"""
File for forms to handle registration, update registration, profile and image
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    """
    Registration form for user
    """
    email = forms.EmailField()

    class Meta:
        """
        Registration forms with its required fields
        """
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """
    User can update their profile
    """
    email = forms.EmailField()

    class Meta:
        """
        User can update forms with its required fields
        """
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """
    User can update their image
    """
    class Meta:
        """
        User can update their image
        """
        model = Profile
        fields = ['image']
