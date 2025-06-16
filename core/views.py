"""
Views for the core app.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import GameSettings, Announcement

def home(request):
    """Home page view."""
    settings = GameSettings.objects.first()
    announcements = Announcement.objects.filter(is_visible=True)[:3]
    
    context = {
        'settings': settings,
        'announcements': announcements,
    }
    return render(request, 'core/home.html', context)

def about(request):
    """About page view."""
    settings = GameSettings.objects.first()
    context = {
        'settings': settings,
    }
    return render(request, 'core/about.html', context)

def rules(request):
    """Rules page view."""
    return render(request, 'core/rules.html')

@login_required
def announcements(request):
    """Announcements page view."""
    announcements = Announcement.objects.filter(is_visible=True)
    context = {
        'announcements': announcements,
    }
    return render(request, 'core/announcements.html', context)
