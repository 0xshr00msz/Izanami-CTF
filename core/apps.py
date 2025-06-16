"""
App configuration for the core app.
"""

import os
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration for the core app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Initialize the Izanami Loop feature when the app is ready.
        This ensures the feature is available by default without requiring a separate setup command.
        """
        # Import here to avoid circular imports
        from django.db import connection
        
        # Check if the tables exist before trying to initialize
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_realitylayer'")
                if not cursor.fetchone():
                    # Tables don't exist yet, so don't try to initialize
                    return
                
            # Only import and run this code if the tables exist
            from django.contrib.auth.models import User
            from core.models import RealityLayer, IzanamiLoop, UserRealityLayer
            
            # Make sure we have at least one reality layer
            first_layer, created = RealityLayer.objects.get_or_create(
                level=1,
                defaults={
                    'name': 'First Illusion',
                    'description': 'The first layer of the Izanami genjutsu. In this reality, things appear normal, but subtle distortions begin to manifest.',
                    'escape_condition': 'Find the hidden pattern in the Academy challenges and submit the escape flag.',
                    'escape_flag': 'izanami{f1rst_l4y3r_br0k3n}'
                }
            )
            
            # Create Izanami Loop for all users
            for user in User.objects.all():
                # Create Izanami Loop for user if it doesn't exist
                IzanamiLoop.objects.get_or_create(
                    user=user,
                    defaults={
                        'current_loop': 1,
                        'loop_iterations': 0,
                        'recognized_patterns': '[]',
                        'distortion_level': 0
                    }
                )
                
                # Create Reality Layer for user if it doesn't exist
                UserRealityLayer.objects.get_or_create(
                    user=user,
                    defaults={
                        'layer': first_layer
                    }
                )
        except Exception:
            # If any error occurs, just skip initialization
            # This prevents errors during migration
            pass
