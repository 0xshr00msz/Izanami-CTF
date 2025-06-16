"""
Management command to create a superuser.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import PlayerProfile

class Command(BaseCommand):
    help = 'Creates a superuser for the Izanami CTF'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@izanami-ctf.com'
        password = 'admin123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))
            return
        
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        # Create player profile for the admin
        PlayerProfile.objects.create(
            user=user,
            sharingan_points=1000,
            chakra_meter=100,
            current_level='uchiha',
            genjutsu_counter=0
        )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Email: {email}'))
        self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
        self.stdout.write(self.style.WARNING('Please change the password after first login!'))
