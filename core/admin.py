"""
Admin configuration for the core app.
"""

from django.contrib import admin
from .models import (
    GameSettings, Announcement, MemoryFragment, IzanamiLoop,
    CollectedFragment, RealityLayer, UserRealityLayer, LoopPattern
)

@admin.register(GameSettings)
class GameSettingsAdmin(admin.ModelAdmin):
    """Admin for game settings."""
    list_display = ('game_name', 'is_active', 'registration_open', 'start_time', 'end_time')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """Admin for announcements."""
    list_display = ('title', 'created_at', 'is_visible')
    list_filter = ('is_visible',)
    search_fields = ('title', 'content')

@admin.register(MemoryFragment)
class MemoryFragmentAdmin(admin.ModelAdmin):
    """Admin for memory fragments."""
    list_display = ('name', 'is_real', 'challenge')
    list_filter = ('is_real',)
    search_fields = ('name', 'description', 'content')

@admin.register(IzanamiLoop)
class IzanamiLoopAdmin(admin.ModelAdmin):
    """Admin for Izanami Loop."""
    list_display = ('user', 'current_loop', 'loop_iterations', 'distortion_level', 'is_trapped')
    list_filter = ('current_loop', 'distortion_level')
    search_fields = ('user__username',)
    
    def is_trapped(self, obj):
        """Check if user is trapped in the loop."""
        return obj.is_trapped()
    is_trapped.boolean = True

@admin.register(CollectedFragment)
class CollectedFragmentAdmin(admin.ModelAdmin):
    """Admin for collected fragments."""
    list_display = ('user', 'fragment', 'collected_at')
    list_filter = ('fragment__is_real',)
    search_fields = ('user__username', 'fragment__name')

@admin.register(RealityLayer)
class RealityLayerAdmin(admin.ModelAdmin):
    """Admin for reality layers."""
    list_display = ('name', 'level')
    list_filter = ('level',)
    search_fields = ('name', 'description')

@admin.register(UserRealityLayer)
class UserRealityLayerAdmin(admin.ModelAdmin):
    """Admin for user reality layers."""
    list_display = ('user', 'layer', 'entered_at')
    list_filter = ('layer',)
    search_fields = ('user__username',)

@admin.register(LoopPattern)
class LoopPatternAdmin(admin.ModelAdmin):
    """Admin for loop patterns."""
    list_display = ('name', 'recognition_flag')
    search_fields = ('name', 'description', 'clue')
