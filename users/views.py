"""
A view file for user profiles
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    """
    Send a message to user when they log in
    """
    if user:
        msg = 'You have securely logged in. \
             Thank you for visiting.'
    messages.add_message(request, messages.INFO, msg)


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    """
    Send a message to user when they log out
    """
    if user:
        msg = 'You have securely logged out.\
            Thank you for visiting.'
        messages.add_message(request, messages.INFO, msg)


def register(request):
    """
    User can register for an account
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your account has been created!\
                     You are now able to log in'
                )
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """
    User can update their profile
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'users/profile.html', context)
