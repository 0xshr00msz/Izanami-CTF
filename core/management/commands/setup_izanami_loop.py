"""
Management command to set up the Izanami Loop feature.
"""

import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from core.models import RealityLayer, LoopPattern, MemoryFragment, IzanamiLoop, UserRealityLayer

class Command(BaseCommand):
    """Command to set up the Izanami Loop feature."""
    help = 'Sets up the Izanami Loop feature by loading initial data and creating necessary objects'

    def handle(self, *args, **options):
        """Handle the command."""
        self.stdout.write(self.style.SUCCESS('Setting up Izanami Loop feature...'))
        
        # Load initial data from fixture
        fixture_path = os.path.join('fixtures', 'izanami_loop_data.json')
        if os.path.exists(fixture_path):
            self.stdout.write(self.style.SUCCESS(f'Loading data from {fixture_path}...'))
            call_command('loaddata', fixture_path)
        else:
            self.stdout.write(self.style.ERROR(f'Fixture file not found: {fixture_path}'))
            return
        
        # Create Izanami Loop and Reality Layer entries for existing users
        users = User.objects.all()
        first_layer = RealityLayer.objects.first()
        
        for user in users:
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
        
        self.stdout.write(self.style.SUCCESS(f'Created Izanami Loop entries for {users.count()} users'))
        self.stdout.write(self.style.SUCCESS('Izanami Loop feature setup complete!'))
