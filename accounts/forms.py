"""
Forms for the accounts app.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PlayerProfile

class UserRegisterForm(UserCreationForm):
    """Form for user registration."""
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    """Form for updating user information."""
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """Form for updating player profile."""
    class Meta:
        model = PlayerProfile
        fields = []  # No fields to update directly
