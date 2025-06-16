"""
Signal handlers for the accounts app.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import connection

@receiver(post_save, sender=User)
def create_izanami_loop(sender, instance, created, **kwargs):
    """
    Create an Izanami Loop for new users.
    This ensures every user is automatically part of the Izanami Loop feature.
    """
    if created:
        # Check if the tables exist before trying to create objects
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_izanamiloop'")
                if not cursor.fetchone():
                    # Tables don't exist yet, so don't try to create objects
                    return
                
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_realitylayer'")
                if not cursor.fetchone():
                    # Tables don't exist yet, so don't try to create objects
                    return
            
            # Only import and run this code if the tables exist
            from core.models import IzanamiLoop, UserRealityLayer, RealityLayer
            
            # Create Izanami Loop for the new user
            IzanamiLoop.objects.create(
                user=instance,
                current_loop=1,
                loop_iterations=0,
                recognized_patterns='[]',
                distortion_level=0
            )
            
            # Get the first reality layer
            first_layer = RealityLayer.objects.first()
            if first_layer:
                # Create UserRealityLayer for the new user
                UserRealityLayer.objects.create(
                    user=instance,
                    layer=first_layer
                )
        except Exception:
            # If any error occurs, just skip creation
            # This prevents errors during migration
            pass
