"""
Core models for the Izanami CTF game.
"""

from django.db import models
from django.contrib.auth.models import User

class GameSettings(models.Model):
    """Global game settings."""
    game_name = models.CharField(max_length=100, default="Izanami: The Endless Loop")
    game_description = models.TextField(default="A web-based CTF game inspired by Itachi's Sharingan Izanami.")
    is_active = models.BooleanField(default=True)
    registration_open = models.BooleanField(default=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Game Settings"
    
    def __str__(self):
        return self.game_name

class Announcement(models.Model):
    """Game announcements."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
